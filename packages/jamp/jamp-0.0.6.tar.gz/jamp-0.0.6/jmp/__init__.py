# Copyright 2020 DeepMind Technologies Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""JMP is a Mixed Precision library for JAX."""

from jmp.loss_scale import all_finite
from jmp.loss_scale import DynamicLossScale
from jmp.loss_scale import LossScale
from jmp.loss_scale import NoOpLossScale
from jmp.loss_scale import select_tree
from jmp.loss_scale import StaticLossScale
from jmp.policy import cast_to_full
from jmp.policy import cast_to_half
from jmp.policy import get_policy
from jmp.policy import half_dtype
from jmp.policy import Policy

__version__ = "0.0.6.dev"

__all__ = (
    "all_finite",
    "DynamicLossScale",
    "LossScale",
    "NoOpLossScale",
    "select_tree",
    "StaticLossScale",
    "cast_to_full",
    "cast_to_half",
    "get_policy",
    "half_dtype",
    "Policy",
)
