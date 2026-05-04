import unittest

class MyTestCase(unittest.TestCase):
    def test_hello(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()