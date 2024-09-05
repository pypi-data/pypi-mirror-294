from VGT_model.ditod_config import add_vit_config
from VGT_model.VGTTrainerTotal import DefaultPredictor
from VGT_model.catalog import MetadataCatalog
from VGT_model.config import get_cfg
import json

from PIL import Image
import numpy as np
import urllib.request

import io
import cv2
import os

from extract_pkl import extract_token
import time


def compute_iou(box1, box2):
    x1, y1, x2, y2 = box1[:4]
    x1_prime, y1_prime, x2_prime, y2_prime = box2[:4]

    # Calculate the coordinates of the intersection rectangle
    x_left = max(x1, x1_prime)
    y_top = max(y1, y1_prime)
    x_right = min(x2, x2_prime)
    y_bottom = min(y2, y2_prime)

    # Check if there is no intersection
    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # Calculate the area of the intersection rectangle
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # Calculate the area of both bounding boxes
    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x2_prime - x1_prime) * (y2_prime - y1_prime)

    # Calculate the IoU
    iou = intersection_area / float(box1_area + box2_area - intersection_area)
    return iou


def remove_low_score_overlapping_boxes(bounding_boxes, sorted_class, iou_threshold=0.5):
    # Sort bounding boxes by the score in descending order
    sorted_indices = np.argsort(-bounding_boxes[:, 4])
    bounding_boxes = bounding_boxes[sorted_indices]
    sorted_class = sorted_class[sorted_indices]

    selected_boxes = []
    selected_classes = []

    while len(bounding_boxes) > 0:
        current_box = bounding_boxes[0]
        current_class = sorted_class[0]

        selected_boxes.append(current_box)
        selected_classes.append(current_class)

        remaining_boxes = []
        remaining_classes = []

        for c, box in enumerate(bounding_boxes[1:]):
            if compute_iou(current_box, box) < iou_threshold:
                remaining_boxes.append(box)
                remaining_classes.append(sorted_class[c + 1])

        bounding_boxes = np.array(remaining_boxes)
        sorted_class = np.array(remaining_classes)

    return np.array(selected_boxes), np.array(selected_classes)


def is_url(string):
    return string.startswith("http://") or string.startswith("https://")


def layout_inference(model, test_image, dt_boxes, rec_res, dt_boxes_layout):
    # merger = OCRTextMerger()

    ocr_result = {}
    ocr_result["dt_boxes"] = dt_boxes_layout
    ocr_result["rec_res"] = rec_res

    grid = extract_token(ocr_result)
    # opencv_image = cv2.imread(test_image)
    output = model(test_image, grid)["instances"]

    boxes = output.pred_boxes
    pred_class = output.pred_classes
    scores = output.scores

    sorted_box = []
    sorted_class = []
    for c, box in enumerate(boxes):
        class_num = pred_class[c].cpu().tolist()

        listed_box = box.cpu().tolist()
        listed_box.extend([scores[c].cpu().tolist()])

        sorted_box.append(listed_box)
        sorted_class.append(class_num)

    sorted_box = np.array(sorted_box)
    sorted_class = np.array(sorted_class)

    filtered_boxes, filtered_classes = remove_low_score_overlapping_boxes(
        sorted_box, sorted_class, iou_threshold=0.1
    )

    centers = (filtered_boxes[:, :2] + filtered_boxes[:, 2:4]) / 2
    sorted_indices = np.lexsort((centers[:, 0], centers[:, 1]))

    sorted_box = filtered_boxes[sorted_indices]
    sorted_class = filtered_classes[sorted_indices]

    boxes = []
    class_name = []
    for c, box in enumerate(sorted_box):
        class_num = sorted_class[c]
        name = md.thing_classes[class_num]

        x0 = box[0]
        y0 = box[1]
        x1 = box[2]
        y1 = box[3]
        box_list = [x0, y0, x1, y1, name]

        boxes.append(box_list)
        class_name.append(name)

    # TODO: use OCR merger.
    # boxes = merger.sort_boxes_top_to_bottom_left_to_right(boxes)
    return boxes
    # TODO: recover this on azure run()
    # detections = [
    #     {"box": [x1, y1, x3, y3], "lines": [], "rec": [], "boxes": [], "class": cn}
    #     for x1, y1, x3, y3, cn in boxes
    # ]
    # rest_dt_boxes, rest_rec_res = [], []
    #
    # for (x1, y1, x3, y3), (text, conf) in zip(dt_boxes, rec_res):
    #     found = False
    #     for detection in detections:
    #         X1, Y1, X3, Y3 = detection["box"]
    #         if X1 <= (x1 + x3) / 2 <= X3 and Y1 <= (y1 + y3) / 2 <= Y3:
    #             # detection['boxes_rec'].append((x1 - X1, y1 - Y1, x3 - X1, y3 - Y1, text, conf))
    #             detection["boxes"].append((x1, y1, x3, y3))
    #             detection["rec"].append((text, conf))
    #             found = True
    #
    #     if not found:
    #         rest_dt_boxes.append((x1, y1, x3, y3))
    #         rest_rec_res.append((text, conf))
    #
    # for idx, detection in enumerate(detections):
    #     if detection["rec"] and detection["class"] not in ["Picture", "Table"]:
    #         l_boxes, l_texts = merger.group_and_merge_boxes_with_text(
    #             detection["boxes"], detection["rec"]
    #         )
    #         lines = [[*box, text[0]] for box, text in zip(l_boxes, l_texts)]
    #         for line in lines:
    #             detection["lines"].append({"polygon": line[:4], "content": line[4]})
    #
    # m_boxes, m_texts = merger.group_and_merge_boxes_with_text(
    #     rest_dt_boxes, rest_rec_res
    # )
    # lines = [[*box, text[0]] for box, text in zip(m_boxes, m_texts)]
    # general_ocr_resulst = []
    # for line in lines:
    #     general_ocr_resulst.append({"polygon": line[:4], "content": line[4]})
    #     detections.append(
    #         {
    #             "box": line[:4],
    #             "lines": general_ocr_resulst,
    #             "rec": [],
    #             "boxes": [],
    #             "class": "Text",
    #         }
    #     )
    #
    # # delete text in picture and table
    # new_detections = []
    # for detection in detections:
    #     pic_tab = False
    #     box = detection["box"]
    #
    #     x_center = (box[0] + box[2]) / 2
    #     y_center = (box[1] + box[3]) / 2
    #
    #     for det in detections:
    #         if det["class"] in ["Picture", "Table"]:
    #             x0 = det["box"][0]
    #             y0 = det["box"][1]
    #             x1 = det["box"][2]
    #             y1 = det["box"][3]
    #
    #             if x0 < x_center < x1 and y0 < y_center < y1:
    #                 pic_tab = True
    #
    #     if pic_tab == False:
    #         new_dict = {
    #             "box": box,
    #             "lines": detection["lines"],
    #             "rec": detection["rec"],
    #             "boxes": detection["boxes"],
    #             "class": detection["class"],
    #         }
    #         new_detections.append(new_dict)
    #
    # return detections, new_detections


if __name__ == '__main__':
    target_image = '{"image_url": "dummy-table.jpg"}'
    # target_image = '{"image_url": "https://ultralytics.com/images/bus.jpg"}'
    test_image = json.loads(target_image)["image_url"]
    configs_path = "VGT_cascade_PTM.yaml"
    # opts_path = ["MODEL.WEIGHTS", "model_final.pth"]

    cfg = get_cfg()
    add_vit_config(cfg)
    cfg.merge_from_file(configs_path)
    # cfg.merge_from_list(opts_path)

    md = MetadataCatalog.get(cfg.DATASETS.TEST[0])
    md.set(
        thing_classes=[
            "Text",
            "Formula",
            "Page-footer",
            "Page-header",
            "Picture",
            "Title",
            "Section-header",
            "Table",
            "Caption",
            "Chart",
        ]
    )
    model = DefaultPredictor(cfg)
    # TODO: remove OCR dummy
    dt_boxes, rec_res_origin, dt_boxes_layout = [[153, 10, 222, 47], [28, 38, 72, 63]], ['haha', 'ggyo'], [
        [153, 10, 222, 47], [28, 38, 72, 63]]
    rec_res = [(item, 1) for item in rec_res_origin]
    test_image = cv2.imread(test_image)
    boxes = layout_inference(model, test_image, dt_boxes, rec_res, dt_boxes_layout)
    print(boxes)
