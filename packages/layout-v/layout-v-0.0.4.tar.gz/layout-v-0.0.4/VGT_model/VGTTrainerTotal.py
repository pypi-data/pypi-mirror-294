import torch

import VGT_model.transforms as T
from .checkpoint import DetectionCheckpointer

from .data import detection_utils as utils
from VGT_model.structures import BoxMode
from VGT_model.data.catalog import MetadataCatalog

from VGT_model.VGT import VGT
import numpy as np

from VGT_model.structures import ImageList
from typing import List, Dict
from VGT_model.layers import move_device_like


def torch_memory(device, tag=""):
    # Checks and prints GPU memory
    print(tag, f"{torch.cuda.memory_allocated(device)/1024/1024:.2f} MB USED")
    print(tag, f"{torch.cuda.memory_reserved(device)/1024/1024:.2f} MB RESERVED")
    print(tag, f"{torch.cuda.max_memory_allocated(device)/1024/1024:.2f} MB USED MAX")
    print(
        tag, f"{torch.cuda.max_memory_reserved(device)/1024/1024:.2f} MB RESERVED MAX"
    )
    print("")


class DefaultPredictor:

    def __init__(self, cfg):

        self.cfg = cfg.clone()  # cfg can be modified by model

        self.model = VGT(self.cfg)
        self.model.eval()
        if len(cfg.DATASETS.TEST):
            self.metadata = MetadataCatalog.get(cfg.DATASETS.TEST[0])

        checkpointer = DetectionCheckpointer(self.model)
        checkpointer.load(cfg.MODEL.WEIGHTS)
        # torch.save(self.model, "test.pth")

        self.aug = T.ResizeShortestEdge(
            [cfg.INPUT.MIN_SIZE_TEST, cfg.INPUT.MIN_SIZE_TEST], cfg.INPUT.MAX_SIZE_TEST
        )

        self.input_format = cfg.INPUT.FORMAT
        assert self.input_format in ["RGB", "BGR"], self.input_format
        self.model.cuda()

        self.pixel_mean = [[[127.5000]], [[127.5000]], [[127.5000]]]
        self.pixel_std = [[[127.5000]], [[127.5000]], [[127.5000]]]
        self.size_divisibility = {"square_size": 0}
        self.padding_constraints = 32

    def _move_to_current_device(self, x):
        return move_device_like(x, self.pixel_mean)

    def preprocess_image(self, batched_inputs: List[Dict[str, torch.Tensor]]):
        """
        Normalize, pad and batch the input images.
        """

        images = [self._move_to_current_device(x["image"]) for x in batched_inputs]
        images = [(x - self.pixel_mean) / self.pixel_std for x in images]
        images = ImageList.from_tensors(
            images,
            self.size_divisibility,
            padding_constraints=self.padding_constraints,
        )
        return images

    def __call__(self, original_image, grid):
        with torch.no_grad():
            height, width = original_image.shape[:2]
            image, transforms = T.apply_transform_gens([self.aug], original_image)

            # add grid
            image_shape = image.shape[:2]  # h, w
            image = torch.as_tensor(image.astype("float32").transpose(2, 0, 1))

            sample_inputs = grid

            input_ids = sample_inputs["input_ids"]
            bbox_subword_list = sample_inputs["bbox_texts_list"]

            bbox = []
            for bbox_per_subword in bbox_subword_list:
                text_word = {}
                text_word["bbox"] = bbox_per_subword.tolist()
                text_word["bbox_mode"] = BoxMode.XYWH_ABS
                utils.transform_instance_annotations(text_word, transforms, image_shape)
                bbox.append(text_word["bbox"])

            dataset_dict = {}
            dataset_dict["input_ids"] = input_ids
            dataset_dict["bbox"] = bbox
            dataset_dict["image"] = image
            dataset_dict["height"] = height
            dataset_dict["width"] = width

            # torch.onnx.export(
            #     self.model,  # PyTorch 모델
            #     dataset_dict,  # 샘플 입력 (튜플로 전달)
            #     "model.onnx",  # 출력할 ONNX 파일명
            #     input_names=[
            #         "input_ids",
            #         "bbox",
            #         "image",
            #         "height",
            #         "width",
            #     ],  # 입력 텐서 이름
            #     output_names=["output"],  # 출력 텐서 이름
            #     dynamic_axes=dynamic_axes,
            #     opset_version=17,  # 사용될 ONNX opset 버전
            # )

            # images = self.preprocess_image([dataset_dict])

            predictions = self.model([dataset_dict])[0]

            return predictions
