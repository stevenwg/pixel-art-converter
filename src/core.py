# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pandas as pd
import json
import timeit

class PixelArtConverter:
    def __init__(self):
        self._image = []
        self._dim = []
        self._color_list = {}
        self.result = []
    
    def set_image(self, image):
        self._image = image
    
    def set_color_list(self, color_list):
        with open(color_list, 'r') as f:
            self._color_list = json.load(f)        
    
    def set_width(self, width):
        shape = self._image.shape
        height = int(shape[0] * width / shape[1])
        self._dim = (width, height)

    def run(self):
        self.result = self._image.copy()
        self.result = self._resize(self.result)
        self.result = self._convert(self.result)
        
        return self.result
    
    def _resize(self, image):
        return cv2.resize(image, self._dim, interpolation=cv2.INTER_AREA)
    
    def _convert(self, image):
        result = image.copy()
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                pixel_LAB = np.reshape(cv2.cvtColor(np.reshape(image[i, j], [1, 1, 3]), cv2.COLOR_BGR2LAB), [3])
                colorId = self._find_closest_color(pixel_LAB)
                result[i, j] = np.array([self._color_list[colorId]["rgb"]["b"], self._color_list[colorId]["rgb"]["g"], self._color_list[colorId]["rgb"]["r"]], np.uint8)
        return result
                
    def _find_closest_color(self, pixel_LAB):
        # rgb_list = [rgb["rgb"] for rgb in self._color_list]
        # hsv_list = [hsv["hsv"] for hsv in self._color_list]
        lab_list = [np.array([lab["lab"]["l"], lab["lab"]["a"], lab["lab"]["b"]]) for lab in self._color_list]
        distance_list = [np.linalg.norm(pixel_LAB - lab) for lab in lab_list]
        min_index = np.argmin(distance_list)
        return min_index

    def compute_cow_file(self, image, name):
        with open(name + ".cow", 'w') as f:
            f.write("# ", name)
            f.write("# Generated with Luffy's PIXEL ART CONVERTER")
            f.write("")
            f.write('$x = "\e[49m  ";          #reset color')
            f.write('$t = "$thoughts ";')
            for colorId in range(self._color_list):
                f.write('$', )


def main():
    image = cv2.imread("./test/luffy.jpg")
    
    PAC = PixelArtConverter()
    PAC.set_image(image)
    PAC.set_width(50)
    PAC.set_color_list("./src/256-color-list.json")
    result = PAC.run()
    
    cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
    cv2.imshow("Original", image)
    cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
    cv2.imshow("Result", result)
    cv2.waitKey()

if __name__ == '__main__':
    main()