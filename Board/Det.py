# Tencent is pleased to support the open source community by making ncnn available.
#
# Copyright (C) 2021 THL A29 Limited, a Tencent company. All rights reserved.
#
# Licensed under the BSD 3-Clause License (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import sys
import cv2
import time
import numpy as np
import ncnn
from ncnn.model_zoo import get_model

def draw_detection_objects(image, class_names, objects, min_prob=0.0):
    for obj in objects:
        if obj.prob < min_prob:
            continue

        print(
            "%d = %.5f at %.2f %.2f %.2f x %.2f\n"
            % (obj.label, obj.prob, obj.rect.x, obj.rect.y, obj.rect.w, obj.rect.h)
        )

        cv2.rectangle(
            image,
            (int(obj.rect.x), int(obj.rect.y)),
            (int(obj.rect.x + obj.rect.w), int(obj.rect.y + obj.rect.h)),
            (255, 0, 0),
        )
        name=class_names[int(obj.label)]
        text = "%s %.1f%%" % (name, obj.prob * 100)

        label_size, baseLine = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

        x = obj.rect.x
        y = obj.rect.y - label_size[1] - baseLine
        if y < 0:
            y = 0
        if x + label_size[0] > image.shape[1]:
            x = image.shape[1] - label_size[0]

        cv2.rectangle(
            image,
            (int(x), int(y)),
            (int(x + label_size[0]), int(y + label_size[1] + baseLine)),
            (255, 255, 255),
            -1,
        )
        if(name=="person"):
            cv2.putText(
                image,
                text,
                (int(x), int(y + label_size[1])),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )
        else:
            cv2.putText(
                image,
                text,
                (int(x), int(y + label_size[1])),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
            )
    resized=cv2.resize(image,None,None,fx=3,fy=3,interpolation=cv2.INTER_NEAREST)
    cv2.imshow("image", resized)
    cv2.waitKey(1)

def Det():
    cap=cv2.VideoCapture(0)
    cap.set(3,160)
    cap.set(4,120)
    while(True):
        _,m = cap.read()
        net = get_model(
            "nanodet",
            target_size=160,
            prob_threshold=0.4,
            nms_threshold=0.5,
            num_threads=4,
            use_gpu=False,
        )
        objects = net(m)
        draw_detection_objects(m, net.class_names, objects)
