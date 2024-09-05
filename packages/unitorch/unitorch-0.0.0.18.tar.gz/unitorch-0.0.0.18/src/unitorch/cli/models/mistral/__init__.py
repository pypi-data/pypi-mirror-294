# Copyright (c) FULIUCANSHENG.
# Licensed under the MIT License.

# pretrained infos
pretrained_mistral_infos = {
    # mistral
    "mistral-7b-instruct-v0.1": {
        "config": "https://huggingface.co/filipealmeida/Mistral-7B-Instruct-v0.1-sharded/resolve/main/config.json",
        "vocab": "https://huggingface.co/filipealmeida/Mistral-7B-Instruct-v0.1-sharded/resolve/main/tokenizer.model",
        "weight": [
            f"https://huggingface.co/filipealmeida/Mistral-7B-Instruct-v0.1-sharded/resolve/main/pytorch_model-{str(i).rjust(5, '0')}-of-00008.bin"
            for i in range(1, 9)
        ],
    },
    "mistral-7b-instruct-v0.3": {
        "config": "https://huggingface.co/MaziyarPanahi/Mistral-7B-Instruct-v0.3/resolve/main/config.json",
        "vocab": "https://huggingface.co/MaziyarPanahi/Mistral-7B-Instruct-v0.3/resolve/main/tokenizer.model",
        "weight": [
            f"https://huggingface.co/MaziyarPanahi/Mistral-7B-Instruct-v0.3/resolve/main/model-{str(i).rjust(5, '0')}-of-00003.safetensors"
            for i in range(1, 4)
        ],
    },
}

pretrained_mistral_extensions_infos = {}

import unitorch.cli.models.mistral.modeling
import unitorch.cli.models.mistral.processing
from unitorch.cli.models.mistral.modeling import (
    MistralForClassification,
    MistralForGeneration,
)
from unitorch.cli.models.mistral.processing import MistralProcessor
