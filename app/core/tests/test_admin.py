from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        # https://docs.djangoproject.com/en/2.2/topics/testing/tools \
        # /#overview-and-a-quick-example
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='password123',
            name='Test user fullname'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        # the url for admin:core_user_changelist is defined in admin app:
        # https://docs.djangoproject.com/en/3.2/ref/contrib/admin/
        # reverse is used instead of using static URL (/admin/core/user/)
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        # reverse will provide the following url ex.:
        # /admin/core/<self.user.id>/
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEquals(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
