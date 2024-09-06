import unittest
from drcodecover.drcodecover import construct_dsn, init_drcode
import sentry_sdk

class TestDrcodecover(unittest.TestCase):

    def test_construct_dsn(self):
        config = {
            'protocol': 'https',
            'public_key': 'abc123',
            'host': 'sentry.io',
            'port': '443',
            'project_id': '12345'
        }
        dsn = construct_dsn(config)
        expected_dsn = 'https://abc123@sentry.io:443/12345'
        self.assertEqual(dsn, expected_dsn)

    def test_init_drcode(self):
        config = {
            'protocol': 'https',
            'public_key': 'abc123',
            'host': 'sentry.io',
            'port': '443',
            'project_id': '12345'
        }
        try:
            init_drcode(config)
            # Check if Sentry has been initialized correctly
            self.assertIsNotNone(sentry_sdk.Hub.current.client, "Sentry SDK should be initialized")
        except Exception as e:
            self.fail(f'init_drcode raised an exception: {e}')

if __name__ == '__main__':
    unittest.main()
