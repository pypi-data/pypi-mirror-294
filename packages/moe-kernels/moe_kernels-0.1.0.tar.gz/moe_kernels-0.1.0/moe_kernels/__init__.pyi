import torch

def topk_softmax(
    topk_weights: torch.Tensor,
    topk_indices: torch.Tensor,
    token_expert_indices: torch.Tensor,
    gating_output: torch.Tensor,
):
    """
    Apply top-k softmax to the gating outputs.
    """
    ...

def marlin_gemm_moe(
    a: torch.Tensor,
    b_q_weights: torch.Tensor,
    sorted_ids: torch.Tensor,
    topk_weights: torch.Tensor,
    topk_ids: torch.Tensor,
    b_scales: torch.Tensor,
    g_idx: torch.Tensor,
    perm: torch.Tensor,
    workspace: torch.Tensor,
    size_m: int,
    size_n: int,
    size_k: int,
    is_k_full: bool,
    num_experts: int,
    topk: int,
    moe_block_size: int,
    replicate_input: bool,
    apply_weights: bool,
) -> torch.Tensor:
    """
    Apply GEMM to quantized MoE layers.
    """
    ...
