#include <torch/extension.h>

#include "ext.h"

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  m.def("topk_softmax", &topk_softmax,
        "Apply topk softmax to the gating outputs");

#ifndef USE_ROCM
  m.def("marlin_gemm_moe", &marlin_gemm_moe, "Marlin GEMM for MoE layers");
#endif
}
