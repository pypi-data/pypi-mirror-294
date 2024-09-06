# -*- coding: utf-8 -*-
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import numpy as np
from typing import Dict, List, Optional, Tuple
import torch
from torch import nn

from VGT_model.config import configurable
from VGT_model.structures import Instances
from VGT_model.utils.events import get_event_storage

from VGT_model.modeling.meta_arch.rcnn import GeneralizedRCNN

from .Wordnn_embedding import WordnnEmbedding


__all__ = ["VGT"]


def torch_memory(device, tag=""):
    # Checks and prints GPU memory
    print(tag, f"{torch.cuda.memory_allocated(device)/1024/1024:.2f} MB USED")
    print(tag, f"{torch.cuda.memory_reserved(device)/1024/1024:.2f} MB RESERVED")
    print(tag, f"{torch.cuda.max_memory_allocated(device)/1024/1024:.2f} MB USED MAX")
    print(
        tag, f"{torch.cuda.max_memory_reserved(device)/1024/1024:.2f} MB RESERVED MAX"
    )
    print("")


class VGT(GeneralizedRCNN):

    @configurable
    def __init__(
        self,
        *,
        vocab_size: int = 30552,
        hidden_size: int = 768,
        embedding_dim: int = 64,
        bros_embedding_path: str = "",
        use_pretrain_weight: bool = True,
        use_UNK_text: bool = False,
        **kwargs,
    ):

        super().__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.Wordgrid_embedding = WordnnEmbedding(
            vocab_size,
            hidden_size,
            embedding_dim,
            bros_embedding_path,
            use_pretrain_weight,
            use_UNK_text,
        )

    @classmethod
    def from_config(cls, cfg):
        ret = super().from_config(cfg)
        ret.update(
            {
                "vocab_size": cfg.MODEL.WORDGRID.VOCAB_SIZE,
                "hidden_size": cfg.MODEL.WORDGRID.HIDDEN_SIZE,
                "embedding_dim": cfg.MODEL.WORDGRID.EMBEDDING_DIM,
                "bros_embedding_path": cfg.MODEL.WORDGRID.MODEL_PATH,
                "use_pretrain_weight": cfg.MODEL.WORDGRID.USE_PRETRAIN_WEIGHT,
                "use_UNK_text": cfg.MODEL.WORDGRID.USE_UNK_TEXT,
            }
        )
        return ret

    # def forward(self, batched_inputs, images):
    #     result = self.inference(batched_inputs, images)
    #     return result

    # def inference(
    #     self,
    #     batched_inputs: List[Dict[str, torch.Tensor]],
    #     images,
    #     detected_instances: Optional[List[Instances]] = None,
    #     do_postprocess: bool = True,
    # ):

    #     assert not self.training

    #     chargrid = self.Wordgrid_embedding(images, batched_inputs)
    #     features = self.backbone(images, chargrid)

    #     if detected_instances is None:  # None
    #         if self.proposal_generator is not None:  # not None
    #             proposals, _ = self.proposal_generator(images, features, None)
    #         results, _ = self.roi_heads(images, features, proposals, None)

    #     return results

    def forward(self, batched_inputs):
        result = self.inference(batched_inputs)
        return result

    def inference(
        self,
        batched_inputs: List[Dict[str, torch.Tensor]],
        detected_instances: Optional[List[Instances]] = None,
        do_postprocess: bool = True,
    ):

        """
        Run inference on the given inputs.

        Args:
            batched_inputs (list[dict]): same as in :meth:`forward`
            detected_instances (None or list[Instances]): if not None, it
                contains an `Instances` object per image. The `Instances`
                object contains "pred_boxes" and "pred_classes" which are
                known boxes in the image.
                The inference will then skip the detection of bounding boxes,
                and only predict other per-ROI outputs.
            do_postprocess (bool): whether to apply post-processing on the outputs.

        Returns:
            When do_postprocess=True, same as in :meth:`forward`.
            Otherwise, a list[Instances] containing raw network outputs.
        """
        assert not self.training

        images = self.preprocess_image(batched_inputs)
        chargrid = self.Wordgrid_embedding(images.tensor, batched_inputs)
        features = self.backbone(images.tensor, chargrid)

        if detected_instances is None:
            if self.proposal_generator is not None:
                proposals, _ = self.proposal_generator(images, features, None)
            else:
                assert "proposals" in batched_inputs[0]
                proposals = [x["proposals"].to(self.device) for x in batched_inputs]

            results, _ = self.roi_heads(images, features, proposals, None)
        else:
            detected_instances = [x.to(self.device) for x in detected_instances]
            results = self.roi_heads.forward_with_given_boxes(
                features, detected_instances
            )

        if do_postprocess:
            assert (
                not torch.jit.is_scripting()
            ), "Scripting is not supported for postprocess."
            return GeneralizedRCNN._postprocess(
                results, batched_inputs, images.image_sizes
            )
        else:
            return results
