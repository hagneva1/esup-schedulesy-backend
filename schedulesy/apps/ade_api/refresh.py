import json
import os
import time
from collections import OrderedDict

from django.conf import settings

from schedulesy.decorators import MemoizeWithTimeout
from .ade import ADEWebAPI, Config
from .models import Resource, Fingerprint


class Flatten:
    def __init__(self, data):
        self.data = data
        self.f_data = OrderedDict()
        self._flatten()

    def _flatten(self, item=None, genealogy=None):
        if not item:
            item = self.data

        if item['tag'] == 'category':
            item['id'] = item['category']
            item['name'] = item['category']

        children_ref = []
        if 'children' in item:
            for child in item['children']:
                me = None
                if 'id' in item:
                    me = list(genealogy) if genealogy is not None else []
                    me.append({'id': item['id'], 'name': item['name']})
                ref = self._flatten(child, me)
                if ref:
                    children_ref.append(ref)

        if 'id' in item:
            key = item['id']
            if key in self.f_data:
                print("Double key {}".format(key))
            else:
                tmp = item.copy()
                if genealogy:
                    tmp['parent'] = genealogy[-1]['id']
                    tmp['genealogy'] = genealogy
                if len(children_ref) > 0:
                    tmp['children'] = children_ref
                self.f_data[key] = tmp
            result = {'id': key, 'name': item['name']}
            result['has_children'] = len(children_ref) > 0
            return result

        return None


class Refresh:
    METHOD_GET_RESOURCE = "getResources"

    def __init__(self):
        self.data = {}
        self.myade = ade_connection()

    def refresh_resource(self, ext_id, operation_id):
        try:
            resource = Resource.objects.get(ext_id=ext_id)
            self._simple_resource_refresh(resource, operation_id)
        except Resource.DoesNotExist:
            for fingerprint in Fingerprint.objects.all():
                fingerprint.fingerprint = "toRefresh"
                fingerprint.save()
                self.refresh_all()
        r = self.myade.getEvents(resources=ext_id, detail=0,
                                 attribute_filter=['id', 'activityId', 'name', 'endHour', 'startHour', 'date',
                                                   'duration', 'lastUpdate', 'category', 'color'])
        if resource is None:
            resource = Resource.objects.get(ext_id=ext_id)
        events = self._reformat_events(r['data'])
        resource.events = events
        resource.save()

    def _simple_resource_refresh(self, resource, operation_id):
        """
        :param Resource resource:
        :return:
        """
        filename = "/tmp/{}-{}.json".format(resource.fields['category'], operation_id)
        if not os.path.exists(filename):
            # May seems brutal but ADE API doesn't give children if object is called individually
            tree = ade_resources(resource.fields['category'], operation_id)
            ade_data = OrderedDict(reversed(list(Flatten(tree['data']).f_data.items())))
            open(filename, 'w').write(json.dumps(ade_data))
        else:
            ade_data = json.loads(open(filename, 'r').read())
        v = ade_data[resource.ext_id]
        if resource.fields != v:
            resource.fields = v
            if "parent" in v:
                if resource.parent_id is None or resource.parent_id != v["parent"]:
                    resource.parent = Resource.objects.get(ext_id=v["parent"])
            else:
                resource.parent = None
            resource.save()

    def _reformat_events(self, data):
        events = []
        classrooms = {}
        resources = {}
        if 'children' in data:
            for element in data['children']:
                element.pop('tag', None)
                element['color'] = '#' + ''.join([format(int(x), '02x') for x in element['color'].split(',')])
                if 'children' in element and len(element['children']) >= 1 and 'children' in element['children'][0]:
                    local_resources = {}
                    for resource in element['children'][0]['children']:
                        # TODO improve plural
                        c_name = resource['category'] + 's'
                        if c_name not in resources:
                            resources[c_name] = {}
                        if c_name not in local_resources:
                            local_resources[c_name] = []
                        tmp_r = {'name': resource['name']}
                        # Adding building to resource
                        if c_name == 'classrooms':
                            if resource['id'] not in classrooms:
                                classrooms[resource['id']] = Resource.objects.get(ext_id=resource['id'])
                            tmp_r['genealogy'] = [x['name'] for x in classrooms[resource['id']].fields['genealogy']][1:]
                        resources[c_name][resource['id']] = tmp_r
                        local_resources[c_name].append(resource['id'])
                    element = {**element, **local_resources}
                    element.pop('children')
                events.append(element)
        result = {'events': events}
        result = {**result, **resources}
        return result

    def refresh_all(self):
        for r_type in ['classroom', 'instructor', 'trainee', 'category5']:
            self.refresh_category(r_type)

    def refresh_category(self, r_type):
        method = Refresh.METHOD_GET_RESOURCE

        tree = ade_resources(r_type)
        n_fp = tree['hash']

        try:
            o_fp = Fingerprint.objects.all().get(ext_id=r_type, method=method)
        except:
            o_fp = None

        key = "{}-{}".format(method, r_type)
        self.data[key] = {'status': 'unchanged', 'fingerprint': n_fp}

        if not o_fp or o_fp.fingerprint != n_fp:
            start = time.clock()
            resources = Resource.objects.all().filter(fields__category=r_type)
            indexed_resources = {r.ext_id: r for r in resources}
            # Dict id reversed to preserve links of parenthood
            test = OrderedDict(reversed(list(Flatten(tree['data']).f_data.items())))

            nb_created = 0
            nb_updated = 0

            # Non existing elements
            for k, v in {key: value for key, value in test.items() if key not in indexed_resources.keys()}.items():
                resource = Resource(ext_id=k, fields=v)
                if "parent" in v:
                    resource.parent = indexed_resources[v["parent"]]
                resource.save()
                indexed_resources[k] = resource
                nb_created += 1

            # Existing elements
            for k, v in {key: value for key, value in test.items() if key in indexed_resources.keys()}.items():
                resource = indexed_resources[k]
                if resource.fields != v:
                    resource.fields = v
                    if "parent" in v:
                        resource.parent = indexed_resources[v["parent"]]
                    resource.save()
                    indexed_resources[k] = resource
                    nb_updated += 1
            if o_fp:
                o_fp.fingerprint = n_fp
            else:
                o_fp = Fingerprint(ext_id=r_type, method=method, fingerprint=n_fp)
            o_fp.save()
            elapsed = time.clock() - start
            self.data[key].update({
                'status': 'modified',
                'updated': nb_updated,
                'created': nb_created,
                'elapsed': elapsed
            })


@MemoizeWithTimeout()
def ade_connection():
    config = Config.create(url=settings.ADE_WEB_API['HOST'],
                           login=settings.ADE_WEB_API['USER'],
                           password=settings.ADE_WEB_API['PASSWORD'])
    connection = ADEWebAPI(**config)
    connection.connect()
    connection.setProject(settings.ADE_WEB_API['PROJECT_ID'])
    return connection


@MemoizeWithTimeout()
def ade_resources(category, operation_id='standard'):
    return ade_connection().getResources(category=category, detail=3, tree=True, hash=True)
