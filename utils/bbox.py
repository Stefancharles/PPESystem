import numpy as np
import os
import cv2
from .colors import get_color

class BoundBox:
    def __init__(self, xmin, ymin, xmax, ymax, c = None, classes = None):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        
        self.c       = c
        self.classes = classes

        self.score = -1
        self.track_id = 0
    @property
    def label(self):
        return np.argmax(self.classes)
        
        return self.label

    def get_score(self):
        if self.score == -1:
            self.score = self.classes[self.label]
            
        return self.score      

def _interval_overlap(interval_a, interval_b):
    x1, x2 = interval_a
    x3, x4 = interval_b

    if x3 < x1:
        if x4 < x1:
            return 0
        else:
            return min(x2,x4) - x1
    else:
        if x2 < x3:
             return 0
        else:
            return min(x2,x4) - x3    

def bbox_iou(box1, box2):
    intersect_w = _interval_overlap([box1.xmin, box1.xmax], [box2.xmin, box2.xmax])
    intersect_h = _interval_overlap([box1.ymin, box1.ymax], [box2.ymin, box2.ymax])  
    
    intersect = intersect_w * intersect_h

    w1, h1 = box1.xmax-box1.xmin, box1.ymax-box1.ymin
    w2, h2 = box2.xmax-box2.xmin, box2.ymax-box2.ymin
    
    union = w1*h1 + w2*h2 - intersect
    
    return float(intersect) / union

def draw_boxes(image, boxes, labels, obj_thresh, quiet=True):
    # persons_with_helmet = 0
    # persons_without_helmet = 0
    for box in boxes:
        label_str = ''
        label = -1
        #
        # for i in range(len(labels)):
        #     if box.classes[i] > obj_thresh:
        #         if label_str != '': label_str += ', '
        #         label_str += (labels[i] + ' ' + str(round(box.get_score()*100, 2)) + '%')
        #         label = i
        #     if not quiet: print(label_str)

        label = np.argmax(box.classes)
        label_str += (labels[label] + ' ' + str(round(box.get_score() * 100, 2)) + '%')
        if not quiet: print(label_str)

        if label >= 0:
            text_size = cv2.getTextSize(label_str, cv2.FONT_HERSHEY_SIMPLEX, 1.1e-3 * image.shape[0], 5)
            width, height = text_size[0][0], text_size[0][1]
            region = np.array([[box.xmin-3,        box.ymin],
                               [box.xmin-3,        box.ymin-height-26],
                               [box.xmin+width+13, box.ymin-height-26],
                               [box.xmin+width+13, box.ymin]], dtype='int32')

            cv2.rectangle(img=image, pt1=(box.xmin,box.ymin), pt2=(box.xmax,box.ymax), color=get_color(label), thickness=5)
            cv2.fillPoly(img=image, pts=[region], color=get_color(label))
            cv2.putText(img=image,
                        text=label_str,
                        org=(box.xmin+13, box.ymin - 13),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1e-3 * image.shape[0],
                        color=(0,0,0),
                        thickness=2)


    #         if label == 1:
    #             persons_with_helmet+=1
    #         if label == 2:
    #             persons_without_helmet+=1
    # print("Persons with helmet = ", persons_with_helmet)
    # print("Persons without helmet = ",persons_without_helmet)

    return image

def draw_box_with_id(image, bbox,id, label, labels, quiet=True):

    label_str = ''

    # label_str += (str(id)+" "+labels[label])
    label_str += (labels[label])

    if not quiet: print(label_str)

    if label >= 0:
        text_size = cv2.getTextSize(label_str, cv2.FONT_HERSHEY_SIMPLEX, 1.1e-3 * image.shape[0], 5)
        width, height = text_size[0][0], text_size[0][1]
        region = np.array([[bbox[0]-3,        bbox[1]],
                           [bbox[0]-3,        bbox[1]-height-26],
                           [bbox[0]+width+13, bbox[1]-height-26],
                           [bbox[0]+width+13, bbox[1]]], dtype='int32')

        cv2.rectangle(image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),
                      color=get_color(label), thickness=2)

        cv2.fillPoly(img=image, pts=[region], color=get_color(label))
        cv2.putText(img=image,
                    text=label_str,
                    org=(int(bbox[0])+13, int(bbox[1]) - 13),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1e-3 * image.shape[0],
                    color=(0,0,0),
                    thickness=2)
    return image