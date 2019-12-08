# -*- coding: utf-8 -*-
import cv2
import numpy as np
import json

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
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                
        
    


    
def main():
    image = cv2.imread("./test/luffy.jpg")
    
    PAC = PixelArtConverter()
    PAC.set_image(image)
    PAC.set_width(50)
    PAC.set_color_list("./src/256-color-list.json")
    image = PAC.run()
    
    
    cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
    cv2.imshow("Result", image)
    cv2.waitKey()

if __name__ == '__main__':
    main()