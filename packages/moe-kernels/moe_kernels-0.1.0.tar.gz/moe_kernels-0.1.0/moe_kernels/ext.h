#pragma once

#include <torch/library.h>

void topk_softmax(torch::Tensor &topk_weights, torch::Tensor &topk_indices,
                  torch::Tensor &token_expert_indices, torch::Tensor &gating_output);

torch::Tensor marlin_gemm_moe(torch::Tensor &a, torch::Tensor &b_q_weights, torch::Tensor &sorted_ids,
                       torch::Tensor &topk_weights, torch::Tensor &topk_ids, torch::Tensor &b_scales,
                       torch::Tensor &g_idx, torch::Tensor &perm, torch::Tensor &workspace,
                       int size_m, int size_n, int size_k, bool is_k_full,
                       int num_experts, int topk, int moe_block_size,
                       bool replicate_input, bool apply_weights);
