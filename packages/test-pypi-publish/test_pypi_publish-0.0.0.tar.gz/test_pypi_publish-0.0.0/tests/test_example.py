import unittest
from src.example_package import greet

class TestExamplePackage(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet(), "Hello, welcome to example_package!")

if __name__ == "__main__":
    unittest.main()
