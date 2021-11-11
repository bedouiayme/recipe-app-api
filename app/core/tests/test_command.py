# patch allow us to to mock the behavior of the django get database function
from unittest.mock import patch
# call_command function allows us to call the command in our source code
from django.core.management import call_command
# import the operational error that django throws
# when the database is unavailable
# and to simulate the database being available or
# not when we run our command
from django.db.utils import OperationalError
# import TestCase
from django.test import TestCase


class CommandTests(TestCase):
    # first test is to test what happens when we
    # call our command and the database is already
    # available
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # we need to simulate the behavior
        # of django when the database is available
        # use patch to mock the connection handler
        # to just return true every time it's called
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
