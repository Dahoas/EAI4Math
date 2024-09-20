import torch
from dataclasses import dataclass
from tqdm import tqdm

from utils import find_smaller_divisor


@dataclass
class NLLemma:
    statement: str
    proof: str
    description: str


######## Utility functions ########

def compute_batched_similarity(sources: torch.tensor, 
                               targets: torch.tensor,
                               batch_size: int,
                               use_gpu=False):
    """
    Computes similarity of each source (in-order) to each target (in-order)
    """
    num_embeddings, embd_dim = sources.shape
    batched_sources = sources.reshape((-1, find_smaller_divisor(num_embeddings, batch_size), embd_dim))
    num_embeddings, embd_dim = targets.shape
    batched_targets = targets.reshape((-1, find_smaller_divisor(num_embeddings, batch_size), embd_dim))
    sims_dict = {i: [] for i in range(len(sources))}
    cnt = 0
    for source_batch in tqdm(batched_sources):
        for target_batch in batched_targets:
            if use_gpu:
                source_batch = source_batch.cuda()
                target_batch = target_batch.cuda()
            sims = (source_batch @ target_batch.T).cpu()
            for i, sample_sim in enumerate(sims):
                sims_dict[cnt+i] += list(sample_sim)
        cnt += len(source_batch)
    return sims_dict
