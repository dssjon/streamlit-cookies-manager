import unittest
from streamlit import cache_data

@cache_data
def cached_function():
    return "cached result"

class TestCache(unittest.TestCase):
    def test_cache_data(self):
        result = cached_function()
        self.assertEqual(result, "cached result")

if __name__ == '__main__':
    unittest.main()