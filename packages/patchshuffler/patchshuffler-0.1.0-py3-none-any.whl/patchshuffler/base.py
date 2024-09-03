import torch
from torch import nn
from abc import ABC, abstractmethod
import os
import time
from einops import rearrange
from typing import Optional

class BaseShuffler(nn.Module, ABC):
    def __init__(self, 
                 input_sample: torch.Tensor, 
                 permute_freq: Optional[int] = 40,
                 num_permuted_samples: Optional[int] = 1000, 
                 gpu_id: Optional[int] = None,
                 permute_strategy: str = "random",
                 save_bank_path: str = "shuffled_idx"):
        super().__init__()
        assert len(input_sample.shape) == 4, f"Data sample must be of shape [B, Channel, Embedding, Patch_num], but got {input_sample.shape}"
        assert permute_strategy in ["random", "vicinity", "farthest"], f"Unknown permutation strategy: {permute_strategy}"
        assert permute_freq > 0, f"Permute frequency must be greater than 0, but got {permute_freq}"
        assert num_permuted_samples > 0, f"Number of permuted samples must be greater than 0, but got {num_permuted_samples}"
        assert permute_freq < 1000, f"Permute frequency must be less than 1000, but got {permute_freq}"
        assert num_permuted_samples < 10000, f"Number of permuted samples must be less than 10000, but got {num_permuted_samples}"

        self.permute_freq = permute_freq
        self.B, self.C, _, self.P = input_sample.shape
        self.num_permutations = num_permuted_samples
        self.permute_strategy = permute_strategy.lower()
        self.save_bank_path = save_bank_path
        if not os.path.exists(self.save_bank_path):
            os.makedirs(self.save_bank_path)
            print(f"Created directory to save shuffled idx output to {self.save_bank_path}")

        file_name = self.load_data_name()

        # Handle device assignment based on gpu_id
        if gpu_id is not None:
            if not torch.cuda.is_available():
                print(f"Warning: CUDA is not available. Using CPU instead of GPU {gpu_id}")
                self.device = torch.device('cpu')
            else:
                self.device = torch.device(f'cuda:{gpu_id}')
        else:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        if os.path.isfile(file_name):
            self.shuffled_idx = torch.load(file_name)
        else:
            print(f"Shuffled idx not found at {file_name}. Creating new shuffled idx...")
            now = time.time()
            self.shuffled_idx = self.construct_shuffled_idx()
            print(f"Time taken to create shuffled idx: {time.time() - now:.3f} seconds")
            self.save_data(self.shuffled_idx, file_name)


        self.shuffled_idx = self.shuffled_idx.to(self.device)
        print(f"Shuffled idx device: {self.shuffled_idx.device}")

    def save_data(self, shuffled_idx, file_name):
        torch.save(shuffled_idx, file_name)
        print(f"Saved shuffled idx to {file_name}")

    def forward(self, X):
        X = rearrange(X, "b c e p -> b e c p")
        rand_idx = torch.randint(0, self.num_permutations - 1, (1,)).to(X.device)
        shuffle_order = self.shuffled_idx[rand_idx]
        expanded_shuffle_order = shuffle_order.expand(X.size(0), X.size(1), -1, -1)
        X_prime = torch.gather(X, 3, expanded_shuffle_order)
        X_shuffled = rearrange(X_prime, "b e c p -> b c e p")
        return X_shuffled

    def load_data_name(self):
        data_name = f"C{self.C}_P{self.P}_permute{str(self.permute_freq).zfill(2)}_{self.permute_strategy}.pt"
        print("*" * 80)
        print(f"Using shuffled idx from {self.save_bank_path}/{data_name}")
        print(f"If file doesn't exist, new shuffled idx will be created and saved to the same path")
        print("*" * 80)
        return f"{self.save_bank_path}/{data_name}"

    @abstractmethod
    def construct_shuffled_idx(self):
        pass