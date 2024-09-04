# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from typing import List

from llama_toolchain.core.datatypes import *  # noqa: F403


def available_inference_providers() -> List[ProviderSpec]:
    return [
        InlineProviderSpec(
            api=Api.inference,
            provider_id="meta-reference",
            pip_packages=[
                "accelerate",
                "blobfile",
                "codeshield",
                "fairscale",
                "fbgemm-gpu==0.8.0",
                "torch",
                "transformers",
                "zmq",
            ],
            module="llama_toolchain.inference.meta_reference",
            config_class="llama_toolchain.inference.meta_reference.MetaReferenceImplConfig",
        ),
        remote_provider_spec(
            api=Api.inference,
            adapter=AdapterSpec(
                adapter_id="ollama",
                pip_packages=["ollama"],
                module="llama_toolchain.inference.adapters.ollama",
            ),
        ),
        InlineProviderSpec(
            api=Api.inference,
            provider_id="fireworks",
            pip_packages=[
                "fireworks-ai",
            ],
            module="llama_toolchain.inference.fireworks",
            config_class="llama_toolchain.inference.fireworks.FireworksImplConfig",
        ),
        InlineProviderSpec(
            api=Api.inference,
            provider_id="together",
            pip_packages=[
                "together",
            ],
            module="llama_toolchain.inference.together",
            config_class="llama_toolchain.inference.together.TogetherImplConfig",
        ),
    ]
