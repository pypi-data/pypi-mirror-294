# Copyright (c) Facebook, Inc. and its affiliates.
import logging

from VGT_model.utils.file_io import PathHandler, PathManager


class ModelCatalog:
    """
    Store mappings from names to third-party models.
    """

    S3_C2_DETECTRON_PREFIX = "https://dl.fbaipublicfiles.com/detectron"

    # MSRA models have STRIDE_IN_1X1=True. False otherwise.
    # NOTE: all BN models here have fused BN into an affine layer.
    # As a result, you should only load them to a model with "FrozenBN".
    # Loading them to a model with regular BN or SyncBN is wrong.
    # Even when loaded to FrozenBN, it is still different from affine by an epsilon,
    # which should be negligible for training.
    # NOTE: all models here uses PIXEL_STD=[1,1,1]
    # NOTE: Most of the BN models here are no longer used. We use the
    # re-converted pre-trained models under detectron2 model zoo instead.
    C2_IMAGENET_MODELS = {
        "MSRA/R-50": "ImageNetPretrained/MSRA/R-50.pkl",
        "MSRA/R-101": "ImageNetPretrained/MSRA/R-101.pkl",
        "FAIR/R-50-GN": "ImageNetPretrained/47261647/R-50-GN.pkl",
        "FAIR/R-101-GN": "ImageNetPretrained/47592356/R-101-GN.pkl",
        "FAIR/X-101-32x8d": "ImageNetPretrained/20171220/X-101-32x8d.pkl",
        "FAIR/X-101-64x4d": "ImageNetPretrained/FBResNeXt/X-101-64x4d.pkl",
        "FAIR/X-152-32x8d-IN5k": "ImageNetPretrained/25093814/X-152-32x8d-IN5k.pkl",
    }

    C2_DATASET_COCO = "coco_2014_train%3Acoco_2014_valminusminival"
    C2_DATASET_COCO_KEYPOINTS = (
        "keypoints_coco_2014_train%3Akeypoints_coco_2014_valminusminival"
    )

    @staticmethod
    def get(name):
        if name.startswith("ImageNetPretrained/"):
            return ModelCatalog._get_c2_imagenet_pretrained(name)
        raise RuntimeError("model not present in the catalog: {}".format(name))

    @staticmethod
    def _get_c2_imagenet_pretrained(name):
        prefix = ModelCatalog.S3_C2_DETECTRON_PREFIX
        name = name[len("ImageNetPretrained/") :]
        name = ModelCatalog.C2_IMAGENET_MODELS[name]
        url = "/".join([prefix, name])
        return url


class ModelCatalogHandler(PathHandler):
    """
    Resolve URL like catalog://.
    """

    PREFIX = "catalog://"

    def _get_supported_prefixes(self):
        return [self.PREFIX]

    def _get_local_path(self, path, **kwargs):
        logger = logging.getLogger(__name__)
        catalog_path = ModelCatalog.get(path[len(self.PREFIX) :])
        logger.info("Catalog entry {} points to {}".format(path, catalog_path))
        return PathManager.get_local_path(catalog_path, **kwargs)

    def _open(self, path, mode="r", **kwargs):
        return PathManager.open(self._get_local_path(path), mode, **kwargs)


PathManager.register_handler(ModelCatalogHandler())
