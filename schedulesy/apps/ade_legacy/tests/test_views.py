import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Customization
from ...ade_api.models import Resource

User = get_user_model()


class CustomizationListTestCase(TestCase):

    databases = '__all__'

    def setUp(self):
        self.view_url = '/legacy/customization.json'
        self.user_url = '/legacy/customization/{username}.json'
        User.objects.create_user('owner', password='pass')
        User.objects.create_superuser('super', 'super@no-reply.com', 'pass')

    def tearDown(self):
        Customization.objects.all().delete()

    def test_list_customizations_with_owner(self):
        Resource.objects.get_or_create(ext_id=1337)
        Customization.objects.create(id=1, directory_id='1', username='owner', resources='1337')
        Customization.objects.create(
            id=2, directory_id='2', username='not_owner')

        self.client.login(username='owner', password='pass')
        response = self.client.get(self.view_url)
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['resources'], '1337')

    def test_list_customizations_consistency(self):
        Customization.objects.create(id=1, directory_id='1', resources='11', username='owner')

        self.client.login(username='owner', password='pass')
        response = self.client.get(self.view_url)
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['resources'], '')

    def test_list_customizations_with_superuser(self):
        Customization.objects.create(id=1, directory_id='1', username='user1')
        Customization.objects.create(id=2, directory_id='2', username='user2')

        self.client.login(username='super', password='pass')
        response = self.client.get(self.view_url)
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

    def test_post_customization_new_object(self):
        response = self.client.post(
            self.view_url, {'directory_id': 1, 'username': 'owner'})

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Customization.objects.get(directory_id=1, username='owner'))

    def test_post_customization_existing_object(self):
        Customization.objects.create(id=1, directory_id='1', username='owner')

        self.client.login(username='owner', password='pass')
        response = self.client.post(
            self.view_url, {'directory_id': 1, 'username': 'owner'})

        self.assertEqual(response.status_code, 409)

    def test_post_customization_update_resources(self):
        Customization.objects.create(id=1, directory_id='1', username='owner')

        self.client.login(username='owner', password='pass')

        data = json.loads(self.client.get(self.view_url).content.decode('utf-8'))
        self.assertEqual(data[0]['resources'], '')

        tmp = Resource.objects.create(ext_id=26908)
        response = self.client.patch(
            self.user_url.format(username='owner'), {"resources":"26908,28135"}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = json.loads(self.client.get(self.view_url).content.decode('utf-8'))
        self.assertEqual(data[0]['resources'], '26908')

        tmp.delete()
        data = json.loads(self.client.get(self.view_url).content.decode('utf-8'))
        self.assertEqual(data[0]['resources'], '')


