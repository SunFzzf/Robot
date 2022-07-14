# 导入opencv工具包
import cv2
# 导入numpy
import numpy as np
# 导入姿势识别器
from PoseDetector import PoseDetector

detector = PoseDetector()

# 方向与个数
squatdir = 0  # 0为站立，1为蹲下
squatcount = 0


def squat(decimg):
    global squatcount,squatdir
    # 读取摄像头，img为每帧图片
    img = decimg

    h, w, c = img.shape
    # 识别姿势
    img = detector.find_pose(img, draw=True)
    # 获取姿势数据
    positions = detector.find_positions(img)

    if positions:
        # 获取下蹲的角度
        angle = detector.find_angle(img, 24, 26, 28)
        # 进度条长度
        bar = np.interp(angle, (50, 170), (w // 2 - 100, w // 2 + 100))
        cv2.rectangle(img, (w // 2 - 100, h - 150),
                      (int(bar), h - 100), (0, 255, 0), cv2.FILLED)
        # 角度小于55度认为下蹲
        if angle <= 55:
            if squatdir == 0:
                squatcount  = squatcount  + 0.5
                squatdir = 1
        # 角度大于120度认为站立
        if angle >= 120:
            if squatdir == 1:
                squatcount = squatcount + 0.5
                squatdir = 0
        cv2.putText(img, str(int(squatcount)), (w // 2, h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 20, cv2.LINE_AA)

    # 打开一个Image窗口显示视频图片
    cv2.imshow('Image', img)
