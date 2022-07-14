import cv2
import numpy as np
from PoseDetector import PoseDetector

detector = PoseDetector()
# 方向和完成次数的变量
pulldir = 0
pullupcount = 0

def pullup(decimg):
    global pullupcount,pulldir
    # 读取视频图片帧
    img = decimg

    # 检测视频图片帧中人体姿势
    img = detector.find_pose(img, draw=True)
    # 获取人体姿势列表数据
    lmslist = detector.find_positions(img)

    # 右手肘的角度
    right_angle = detector.find_angle(img, 12, 14, 16)
    # 以170到20度检测右手肘弯曲的程度
    right_per = np.interp(right_angle, (20, 170), (100, 0))
    # 进度条高度数据
    right_bar = np.interp(right_angle, (20, 170), (200, 400))
    # 使用opencv画进度条和写右手肘弯曲的程度
    cv2.rectangle(img, (1200, 200), (1220, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (1200, int(right_bar)), (1220, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(int(right_per)) + '%', (1190, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # 左手肘的角度
    left_angle = detector.find_angle(img, 11, 13, 15)
    left_per = np.interp(left_angle, (20, 170), (100, 0))
    left_bar = np.interp(left_angle, (20, 170), (200, 400))
    cv2.rectangle(img, (500, 200), (520, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (500, int(left_bar)), (520, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(int(left_per)) + '%', (490, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # 检测个数，我这里设置的是从20%做到80%，就认为是一个
    if (left_per >= 80 and right_per >= 80):
        if pulldir == 0:
            pullupcount = pullupcount + 0.5
            pulldir = 1
    if (left_per <= 20 and right_per <= 20):
        if pulldir == 1:
            pullupcount = pullupcount + 0.5
            pulldir = 0

    # 在视频上显示完成个数
    cv2.putText(img, str(int(pullupcount)), (1000, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 4)

    cv2.imshow('Image', img)
    # cv2.waitKey(1)

