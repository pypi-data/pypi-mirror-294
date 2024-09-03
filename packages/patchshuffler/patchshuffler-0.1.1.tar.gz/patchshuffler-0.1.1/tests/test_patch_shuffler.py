import unittest
import torch
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from patchshuffler.patch_shuffler import PatchShuffler

class TestPatchShuffler(unittest.TestCase):
    def setUp(self):
        self.batch_size = 2
        self.channels = 3
        self.embedding_size = 224
        self.num_patches = 16
        self.input_sample = torch.randn(self.batch_size, self.channels, self.embedding_size, self.num_patches)

    def test_initialization(self):
        shuffler = PatchShuffler(self.input_sample)
        self.assertIsInstance(shuffler, PatchShuffler)

    def test_output_shape(self):
        shuffler = PatchShuffler(self.input_sample)
        output = shuffler(self.input_sample)
        self.assertEqual(output.shape, self.input_sample.shape)

    def test_permute_frequency(self):
        permute_freq = 5
        shuffler = PatchShuffler(self.input_sample, permute_freq=permute_freq)
        self.assertEqual(shuffler.permute_freq, permute_freq)

    def test_permute_strategy(self):
        for strategy in ["random", "vicinity", "farthest"]:
            shuffler = PatchShuffler(self.input_sample, permute_strategy=strategy)
            self.assertEqual(shuffler.permute_strategy, strategy)

    def test_invalid_permute_strategy(self):
        with self.assertRaises(AssertionError):
            PatchShuffler(self.input_sample, permute_strategy="invalid")

    def test_shuffling(self):
        shuffler = PatchShuffler(self.input_sample)
        output = shuffler(self.input_sample)
        
        # Check that the output is not identical to the input
        self.assertFalse(torch.all(output == self.input_sample))
        
        # Check that the shuffling only occurred along the patch dimension
        input_sum = self.input_sample.sum(dim=3)
        output_sum = output.sum(dim=3)
        self.assertTrue(torch.allclose(input_sum, output_sum, atol=1e-6))

    def test_device_cpu(self):
        shuffler = PatchShuffler(self.input_sample, gpu_id=None)
        self.assertEqual(shuffler.device.type, 'cpu')

    @unittest.skipIf(not torch.cuda.is_available(), "CUDA not available")
    def test_device_gpu(self):
        shuffler = PatchShuffler(self.input_sample, gpu_id=0)
        self.assertEqual(shuffler.device.type, 'cuda')

    def test_reproducibility(self):
        torch.manual_seed(42)
        shuffler1 = PatchShuffler(self.input_sample)
        output1 = shuffler1(self.input_sample)

        torch.manual_seed(42)
        shuffler2 = PatchShuffler(self.input_sample)
        output2 = shuffler2(self.input_sample)

        self.assertTrue(torch.all(output1 == output2))

if __name__ == '__main__':
    unittest.main()