# 导入opencv工具包
import cv2
# 导入numpy
import numpy as np
# 导入姿势识别器
from PoseDetector import PoseDetector

# 姿势识别器
detector = PoseDetector()

# 方向与个数
sitdir = 0  # 0为躺下，1为坐起
situpcount = 0


def situp(decimg):
    global situpcount,sitdir
    # 读取摄像头，img为每帧图片
    img = decimg
    h, w, c = img.shape
    # 识别姿势
    img = detector.find_pose(img, draw=True)
    # 获取姿势数据
    positions = detector.find_positions(img)

    if positions:
        # 获取仰卧起坐的角度
        angle = detector.find_angle(img, 11, 23, 25)
        # 进度条长度
        bar = np.interp(angle, (50, 130), (w // 2 - 100, w // 2 + 100))
        cv2.rectangle(img, (w // 2 - 100, h - 150),
                      (int(bar), h - 100), (0, 255, 0), cv2.FILLED)
        # 角度小于55度认为坐起
        if angle <= 55:
            if sitdir == 0:
                situpcount = situpcount + 0.5
                sitdir = 1
        # 角度大于120度认为躺下
        if angle >= 120:
            if sitdir == 1:
                situpcount = situpcount + 0.5
                sitdir = 0
        cv2.putText(img, str(int(situpcount)), (w // 2, h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 20, cv2.LINE_AA)

    # 打开一个Image窗口显示视频图片
    cv2.imshow('Image', img)
