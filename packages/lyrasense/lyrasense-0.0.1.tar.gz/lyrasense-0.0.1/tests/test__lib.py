import unittest
from unittest.mock import patch
from src.lib import Lyrasense

class TestLyrasenseLib(unittest.TestCase):

    @patch('requests.post')
    def test_simple_function(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"job_id": "1234"}
        
        @Lyrasense.function
        def add(a, b):
            return a + b
        
        job_id = add(3, 5)
        self.assertEqual(job_id, "1234")
        mock_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()
