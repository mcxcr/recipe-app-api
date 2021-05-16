from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        """
        Mandatory func to be able to test other funcs inside the CLASS...
        """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@mcx.ink',
            password='Test@123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='testuser@mcx.ink',
            password='Test@12345',
            name='Test User full name'
        )

    def test_users_listed(self):
        """ Tests that users are listed on user page. """
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """ Test that user edit page works """
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/ID_of_User
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ Test that create users page work """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
