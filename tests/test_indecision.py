import unittest

import indecision


class IndecisionTestCase(unittest.TestCase):

    def setUp(self):
        self.app = indecision.app.test_client()

    # def test_index(self):
    #     rv = self.app.get('/')
    #     self.assertIn('Welcome to indecision', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
