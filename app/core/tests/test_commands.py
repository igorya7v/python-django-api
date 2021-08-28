from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # https://github.com/django/django/blob/ \
        # 11b8c30b9e02ef6ecb996ad3280979dfeab700fa/django/db/utils.py#L195
        with patch('django.db.utils.ConnectionHandler.__getitem__') as getitem:
            getitem.return_value = True
            # https://docs.djangoproject.com/en/3.2/ref/django-admin/ \
            # #running-management-commands-from-your-code
            call_command('wait_for_db')
            self.assertEqual(getitem.call_count, 1)

    # the @patch decorator acts the same like mocking above ln:14
    # the mocked method have to be passed to the test method, see timesleep arg
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, timesleep):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as getitem:
            # The first 5 times "OperationalError" will be raised,
            # after 5 times it will return "True" (no OperationalError)
            getitem.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(getitem.call_count, 6)
