import os
import json
from transformers import AutoTokenizer, LayoutLMForMaskedLM
import pickle
import numpy as np


tokenizer = AutoTokenizer.from_pretrained("layout_detector/layout_configs")


def extract_token(line):
    dt_boxes = np.array(line["dt_boxes"])
    rec_res = [str(word) for word in line["rec_res"]]
    rec_res_ = [str(word[0]) for word in line["rec_res"]]
    token_boxes = []
    xywh = []
    for c, box in enumerate(dt_boxes):
        # x, y, w, h
        bb = [box[0], box[1], box[2], box[3]]  #  - box[0], box[3] - box[1]]
        ## upstage
        # bb = [box[0], box[1], box[2] - box[0], box[3] - box[1]]

        if c >= len(rec_res):
            continue

        if len(rec_res[c][-4:-1]) > 2:
            if rec_res[c][-4:-1] == "nan":
                continue

        xywh.append(bb)

        word_token = tokenizer.tokenize(str(eval(rec_res[c])[0]))
        token_boxes.extend([bb] * len(word_token))

    encoding = tokenizer([str(" ".join(rec_res_))], return_tensors="pt")
    input_ids = encoding["input_ids"]

    input_list = []
    for c, i in enumerate(input_ids[0]):
        if c == 0:
            continue
        if c == len(input_ids[0]) - 1:
            continue

        input_list.append(i.item())

    res = {
        "input_ids": np.array(input_list),
        "bbox_subword_list": np.array(token_boxes),
        "texts": rec_res_,
        "bbox_texts_list": np.array(xywh),
    }
    return res


if __name__ == "__main__":
    json = "IMG_1721.json"
    extract_token(json)


