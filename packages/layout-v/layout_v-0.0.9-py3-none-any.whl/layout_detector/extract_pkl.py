import os
import json
from transformers import AutoTokenizer, LayoutLMForMaskedLM
import pickle
import numpy as np


tokenizer = AutoTokenizer.from_pretrained("layoutlm")


def extract_token(line):
    # with open(json_file) as file_data:
    #     line = file_data.readline()
    # print(line)
    # for line in f:
    # dt_boxes = np.array(eval(line)['dt_boxes'])
    # rec_res = [str(word) for word in eval(line)['rec_res']]
    # rec_res_ = [str(word[0]) for word in eval(line)['rec_res'] ]

    dt_boxes = np.array(line["dt_boxes"])
    rec_res = [str(word) for word in line["rec_res"]]
    rec_res_ = [str(word[0]) for word in line["rec_res"]]
    token_boxes = []
    xywh = []
    # print('dt_boxes: ', len(dt_boxes))
    # print('rec_res: ', len(rec_res))
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

        # print('rec_res: ', rec_res)
        # print('rec_res[c]1: ', rec_res[c][-4:-1])
        # print('rec_res[c]:2 ', eval(rec_res[c])[0])
        # print('rec_res[c]: 3', eval(rec_res[c])[1])
        # print('bb: ', bb)
        # print(rec_res[c])
        # print(rec_res[c][-4:-1])
        # print(len(rec_res[c][-4:-1]))

        # print('eval(rec_res[c]): ', eval(rec_res[c]))
        # print('str(eval(rec_res[c])): ', str(eval(rec_res[c])))
        # print('str(eval(rec_res[c])[0]): ', str(eval(rec_res[c])[0]))
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
    # print('res: ', res)
    # with open('./IMG_1721.pdf.pkl','wb') as fw:
    #     pickle.dump(res, fw)
    return res


if __name__ == "__main__":
    json = "IMG_1721.json"
    extract_token(json)


