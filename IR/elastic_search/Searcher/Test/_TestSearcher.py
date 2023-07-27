import unittest
from my_module.searcher import Searcher

class TestSearcher(unittest.TestCase):
    def setUp(self):
        self.index_name = "test-index"
        self.searcher = Searcher(index_name=self.index_name)

    def test_search(self):
        query_embeddings = [0.2, 0.4, 0.1]  # Placeholder for actual query embeddings
        size = 5
        results = self.searcher.search(query_embeddings, size)

        self.assertEqual(len(results), size)
        for hit in results:
            self.assertIn("_source", hit)
            self.assertIn("id", hit["_source"])
            self.assertIn("title", hit["_source"])
            self.assertIn("text", hit["_source"])
            self.assertNotIn("embeddings", hit["_source"])

if __name__ == '__main__':
    unittest.main()
