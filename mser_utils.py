import cv2
import numpy as np

from .image_utils import to_gray

        
def draw_ellipses(im, ellipses): 
    for e in ellipses:
        cv2.ellipse(im, e, (255, 255, 0) if im.ndim == 3 else 255,1)
    return 

def draw_hulls(im, hulls): 
    cv2.polylines(im, hulls, 1, (0, 255, 0) if im.ndim == 3 else 255, thickness=1)       
    return 

def fill_hulls(im, hulls): 
    for hull in hulls: 
        cv2.fillPoly(im, [hull], (0, 255, 0) if im.ndim == 3 else 255)
    return 

class MSER:
    def __init__(self):
        
        # Compute MSER features on the rgb image
        mser_delta = 5
        mser_min_area = 100
        mser_max_area = 160*120
        mser_max_variation = 0.25
        mser_min_diversity = 0.2
        mser_max_evolution = 200 # 0.001 # 0.003
        mser_area_threshold = 1.01
        mser_min_margin = 0.003
        mser_edge_blur_size = 11

        self.mser = cv2.MSER(_min_area=mser_min_area, _max_area=mser_max_area, _max_evolution=mser_max_evolution,
                             _edge_blur_size=mser_edge_blur_size)

    def detect(self, im): 
        return self.mser.detect(im)

    def hulls(self, im):
        regions = self.detect(im)
        return [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]

    def ellipses(self, im): 
        hulls = self.hulls(im)
        return [cv2.fitEllipse(contours_from_endpoints(hull.reshape(-1,2),10))
                for hull in hulls]
