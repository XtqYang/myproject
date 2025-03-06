# test_h5_tk.py
import unittest
from myproject.spiders.m_h5_tk import H5TkExtractor

class TestH5TK(unittest.TestCase):
    def test_token_generation(self):
        extractor = H5TkExtractor()
        tokens = extractor.get_h5_tk("test_id")
        self.assertNotIn("未找到", tokens[0])
        self.assertNotIn("未找到", tokens[1])

if __name__ == '__main__':
    unittest.main()