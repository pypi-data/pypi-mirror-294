# Copyright (c) FULIUCANSHENG.
# Licensed under the MIT License.

import torch
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from torch.cuda.amp import autocast

from unitorch.models.peft.diffusers import (
    Stable3LoraForText2ImageGeneration as _Stable3LoraForText2ImageGeneration,
)
from unitorch.utils import pop_value, nested_dict_value
from unitorch.cli import (
    cached_path,
    add_default_section_for_init,
    add_default_section_for_function,
    register_model,
)
from unitorch.cli.models import DiffusionOutputs, LossOutputs
from unitorch.cli.models import diffusion_model_decorator
from unitorch.cli.models.diffusers import (
    pretrained_stable_infos,
    pretrained_stable_extensions_infos,
    load_weight,
)


@register_model(
    "core/model/diffusers/peft/lora/text2image/stable_3", diffusion_model_decorator
)
class Stable3LoraForText2ImageGeneration(_Stable3LoraForText2ImageGeneration):
    def __init__(
        self,
        config_path: str,
        text_config_path: str,
        text2_config_path: str,
        text3_config_path: str,
        vae_config_path: str,
        scheduler_config_path: str,
        controlnet_configs_path: Union[str, List[str]] = None,
        quant_config_path: Optional[str] = None,
        image_size: Optional[int] = None,
        in_channels: Optional[int] = None,
        out_channels: Optional[int] = None,
        num_train_timesteps: Optional[int] = 1000,
        num_infer_timesteps: Optional[int] = 50,
        snr_gamma: Optional[float] = 5.0,
        lora_r: Optional[int] = 16,
        lora_alpha: Optional[int] = 32,
        enable_text_adapter: Optional[bool] = True,
        enable_transformer_adapter: Optional[bool] = True,
        seed: Optional[int] = 1123,
    ):
        super().__init__(
            config_path=config_path,
            text_config_path=text_config_path,
            text2_config_path=text2_config_path,
            text3_config_path=text3_config_path,
            vae_config_path=vae_config_path,
            scheduler_config_path=scheduler_config_path,
            controlnet_configs_path=controlnet_configs_path,
            quant_config_path=quant_config_path,
            image_size=image_size,
            in_channels=in_channels,
            out_channels=out_channels,
            num_train_timesteps=num_train_timesteps,
            num_infer_timesteps=num_infer_timesteps,
            snr_gamma=snr_gamma,
            lora_r=lora_r,
            lora_alpha=lora_alpha,
            enable_text_adapter=enable_text_adapter,
            enable_transformer_adapter=enable_transformer_adapter,
            seed=seed,
        )

    @classmethod
    @add_default_section_for_init("core/model/diffusers/peft/lora/text2image/stable_3")
    def from_core_configure(cls, config, **kwargs):
        config.set_default_section("core/model/diffusers/peft/lora/text2image/stable_3")
        pretrained_name = config.getoption("pretrained_name", "stable-v3-medium")
        pretrained_infos = nested_dict_value(pretrained_stable_infos, pretrained_name)

        config_path = config.getoption("config_path", None)
        config_path = pop_value(
            config_path,
            nested_dict_value(pretrained_infos, "transformer", "config"),
        )
        config_path = cached_path(config_path)

        text_config_path = config.getoption("text_config_path", None)
        text_config_path = pop_value(
            text_config_path,
            nested_dict_value(pretrained_infos, "text", "config"),
        )
        text_config_path = cached_path(text_config_path)

        text2_config_path = config.getoption("text2_config_path", None)
        text2_config_path = pop_value(
            text2_config_path,
            nested_dict_value(pretrained_infos, "text2", "config"),
        )
        text2_config_path = cached_path(text2_config_path)

        text3_config_path = config.getoption("text3_config_path", None)
        text3_config_path = pop_value(
            text3_config_path,
            nested_dict_value(pretrained_infos, "text3", "config"),
        )
        text3_config_path = cached_path(text3_config_path)

        vae_config_path = config.getoption("vae_config_path", None)
        vae_config_path = pop_value(
            vae_config_path,
            nested_dict_value(pretrained_infos, "vae", "config"),
        )
        vae_config_path = cached_path(vae_config_path)

        scheduler_config_path = config.getoption("scheduler_config_path", None)
        scheduler_config_path = pop_value(
            scheduler_config_path,
            nested_dict_value(pretrained_infos, "scheduler"),
        )
        scheduler_config_path = cached_path(scheduler_config_path)

        quant_config_path = config.getoption("quant_config_path", None)
        if quant_config_path is not None:
            quant_config_path = cached_path(quant_config_path)

        image_size = config.getoption("image_size", None)
        in_channels = config.getoption("in_channels", None)
        out_channels = config.getoption("out_channels", None)
        num_train_timesteps = config.getoption("num_train_timesteps", 1000)
        num_infer_timesteps = config.getoption("num_infer_timesteps", 50)
        enable_text_adapter = config.getoption("enable_text_adapter", True)
        enable_transformer_adapter = config.getoption(
            "enable_transformer_adapter", True
        )
        seed = config.getoption("seed", 1123)

        inst = cls(
            config_path=config_path,
            text_config_path=text_config_path,
            text2_config_path=text2_config_path,
            text3_config_path=text3_config_path,
            vae_config_path=vae_config_path,
            scheduler_config_path=scheduler_config_path,
            quant_config_path=quant_config_path,
            image_size=image_size,
            in_channels=in_channels,
            out_channels=out_channels,
            num_train_timesteps=num_train_timesteps,
            num_infer_timesteps=num_infer_timesteps,
            enable_text_adapter=enable_text_adapter,
            enable_transformer_adapter=enable_transformer_adapter,
            seed=seed,
        )

        weight_path = config.getoption("pretrained_weight_path", None)

        state_dict = None
        if weight_path is None and pretrained_infos is not None:
            state_dict = [
                load_weight(
                    nested_dict_value(pretrained_infos, "transformer", "weight"),
                    prefix_keys={"": "transformer."},
                    replace_keys={
                        "to_k.": "to_k.base_layer.",
                        "to_q.": "to_q.base_layer.",
                        "to_v.": "to_v.base_layer.",
                        "to_out.0.": "to_out.0.base_layer.",
                    }
                    if enable_transformer_adapter
                    else {},
                ),
                load_weight(
                    nested_dict_value(pretrained_infos, "text", "weight"),
                    prefix_keys={"": "text."},
                    replace_keys={
                        "q_proj.": "q_proj.base_layer.",
                        "v_proj.": "v_proj.base_layer.",
                        "out_proj.": "out_proj.base_layer.",
                    }
                    if enable_text_adapter
                    else {},
                ),
                load_weight(
                    nested_dict_value(pretrained_infos, "text2", "weight"),
                    prefix_keys={"": "text2."},
                    replace_keys={
                        "q_proj.": "q_proj.base_layer.",
                        "v_proj.": "v_proj.base_layer.",
                        "out_proj.": "out_proj.base_layer.",
                    }
                    if enable_text_adapter
                    else {},
                ),
                load_weight(
                    nested_dict_value(pretrained_infos, "text3", "weight"),
                    prefix_keys={"": "text3."},
                    replace_keys={
                        "q_proj.": "q_proj.base_layer.",
                        "v_proj.": "v_proj.base_layer.",
                        "out_proj.": "out_proj.base_layer.",
                    }
                    if enable_text_adapter
                    else {},
                ),
                load_weight(
                    nested_dict_value(pretrained_infos, "vae", "weight"),
                    prefix_keys={"": "vae."},
                ),
            ]
        elif weight_path is not None:
            state_dict = load_weight(weight_path)

        pretrained_lora_weight_path = config.getoption(
            "pretrained_lora_weight_path", None
        )
        if pretrained_lora_weight_path is not None:
            lora_state_dict = load_weight(pretrained_lora_weight_path)
            if state_dict is not None:
                state_dict.append(lora_state_dict)
            else:
                state_dict = lora_state_dict

        if state_dict is not None:
            inst.from_pretrained(state_dict=state_dict)
        return inst

    # @autocast()
    def forward(
        self,
        pixel_values: torch.Tensor,
        input_ids: torch.Tensor,
        input2_ids: torch.Tensor,
        input3_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        attention2_mask: Optional[torch.Tensor] = None,
        attention3_mask: Optional[torch.Tensor] = None,
    ):
        loss = super().forward(
            input_ids=input_ids,
            input2_ids=input2_ids,
            input3_ids=input3_ids,
            pixel_values=pixel_values,
            attention_mask=attention_mask,
            attention2_mask=attention2_mask,
            attention3_mask=attention3_mask,
        )
        return LossOutputs(loss=loss)

    @add_default_section_for_function(
        "core/model/diffusers/peft/lora/text2image/stable_3"
    )
    # @autocast()
    def generate(
        self,
        input_ids: torch.Tensor,
        input2_ids: torch.Tensor,
        input3_ids: torch.Tensor,
        negative_input_ids: torch.Tensor,
        negative_input2_ids: torch.Tensor,
        negative_input3_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        attention2_mask: Optional[torch.Tensor] = None,
        attention3_mask: Optional[torch.Tensor] = None,
        negative_attention_mask: Optional[torch.Tensor] = None,
        negative_attention2_mask: Optional[torch.Tensor] = None,
        negative_attention3_mask: Optional[torch.Tensor] = None,
        height: Optional[int] = 1024,
        width: Optional[int] = 1024,
        guidance_scale: Optional[float] = 5.0,
    ):
        outputs = super().generate(
            input_ids=input_ids,
            input2_ids=input2_ids,
            input3_ids=input3_ids,
            negative_input_ids=negative_input_ids,
            negative_input2_ids=negative_input2_ids,
            negative_input3_ids=negative_input3_ids,
            attention_mask=attention_mask,
            attention2_mask=attention2_mask,
            attention3_mask=attention3_mask,
            negative_attention_mask=negative_attention_mask,
            negative_attention2_mask=negative_attention2_mask,
            negative_attention3_mask=negative_attention3_mask,
            height=height,
            width=width,
            guidance_scale=guidance_scale,
        )

        return DiffusionOutputs(outputs=outputs.images)
