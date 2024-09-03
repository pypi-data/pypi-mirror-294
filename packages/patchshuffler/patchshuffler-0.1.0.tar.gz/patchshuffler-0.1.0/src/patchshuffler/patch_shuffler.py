import numpy as np
import torch
import random
from .base import BaseShuffler
from typing import Optional

class PatchShuffler(BaseShuffler):
    def __init__(self, 
                 input_sample: torch.Tensor, 
                 permute_freq: Optional[int] = 40,
                 num_permuted_samples: Optional[int] = 1000, 
                 gpu_id: Optional[int] = None,
                 permute_strategy: str = "random",
                 save_bank_path: str = "shuffled_idx"):
        super().__init__(input_sample, permute_freq, num_permuted_samples, gpu_id, permute_strategy, save_bank_path)

    def construct_shuffled_idx(self) -> torch.Tensor:
        data = np.arange(0, self.P)

        total_shuffled_idx = []
        print(f"Constructing shuffled idx with strategy {self.permute_strategy} / freq:{self.permute_freq} for {self.num_permutations} times")
        for _ in range(self.num_permutations):
            shuffled_idx_list = []
            for _ in range(self.C):
                copy_data = data.copy()
                num_patches = len(copy_data)
                for _ in range(self.permute_freq):
                    if self.permute_strategy == "random":
                        idx1, idx2 = random.sample(range(num_patches), 2)
                    elif self.permute_strategy == "vicinity":
                        idx1 = random.randint(0, num_patches - 2)
                        idx2 = idx1 + 1
                    elif self.permute_strategy == "farthest":
                        idx1, idx2 = random.sample(range(num_patches), 2)
                        while abs(idx1 - idx2) < 2:
                            idx1, idx2 = random.sample(range(num_patches), 2)
                    else:
                        raise ValueError(f"Unknown permutation strategy: {self.permute_strategy}")

                    copy_data[idx1], copy_data[idx2] = copy_data[idx2], copy_data[idx1]

                shuffled_idx_list.append(copy_data)
            shuffled_idx_list = np.stack(shuffled_idx_list, axis=0)
            total_shuffled_idx.append(shuffled_idx_list)
        total_shuffled_idx = torch.tensor(np.stack(total_shuffled_idx, axis=0), device=self.device)

        return total_shuffled_idx