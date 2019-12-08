# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pandas as pd
import json

def color_list_BGR2LAB():
    with open("./src/256-color-list.json", 'r') as f:
        color_list = json.load(f)
    bgr_list = [np.reshape(np.array([rgb["rgb"]["b"], rgb["rgb"]["g"], rgb["rgb"]["r"]], np.uint8), [1, 1, 3]) for rgb in color_list]
    lab_list = [cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)[0, 0, :].tolist() for bgr in bgr_list]
    [color.update({"lab":{"l":lab[0], "a":lab[1], "b":lab[2]}}) for color, lab in zip(color_list, lab_list)]
    with open("./src/256-color-list-copy.json", 'w') as f:
        json.dump(color_list, f, ensure_ascii=False, indent=4)
        
if __name__ == '__main__':
    color_list_BGR2LAB()