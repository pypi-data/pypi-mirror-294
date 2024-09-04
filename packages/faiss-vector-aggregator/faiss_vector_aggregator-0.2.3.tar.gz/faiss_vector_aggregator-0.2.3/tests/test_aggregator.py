import unittest
import os
import shutil
from faiss_vector_aggregator import aggregate_embeddings

class TestFaissVectorAggregator(unittest.TestCase):

    def setUp(self):
        # Setup paths for the test
        self.input_folder = "test_data/input"
        self.output_folder = "test_data/output"
        self.column_name = "id"

        # Ensure output folder is clean
        if os.path.exists(self.output_folder):
            shutil.rmtree(self.output_folder)
        os.makedirs(self.output_folder)

    def test_aggregate_embeddings(self):
        # Run the aggregation
        output_index_path, output_metadata_path = aggregate_embeddings(
            self.input_folder, self.column_name, self.output_folder
        )

        # Check that output files exist
        self.assertTrue(os.path.exists(output_index_path), "Faiss index file not found.")
        self.assertTrue(os.path.exists(output_metadata_path), "Metadata file not found.")

        # Additional checks could include validating the content of the index and metadata
        # For example, ensure the index has the expected number of embeddings
        # or that the metadata contains the expected ids.

    def tearDown(self):
        # Clean up after the test
        if os.path.exists(self.output_folder):
            shutil.rmtree(self.output_folder)

if __name__ == '__main__':
    unittest.main()
