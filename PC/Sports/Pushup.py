# 导入opencv工具包
import cv2
# 导入numpy
import numpy as np
# 导入姿势识别器
from PoseDetector import PoseDetector

# 姿势识别器
detector = PoseDetector()

# 方向与个数
pushdir = 0  # 0为下，1为上
pushcount = 0


def pushup(decimg):
    global pushcount,pushdir
    # 读取摄像头，img为每帧图片
    img = decimg

    h, w, c = img.shape
    # 识别姿势
    img = detector.find_pose(img, draw=True)
    # 获取姿势数据
    positions = detector.find_positions(img)

    if positions:
        # 获取俯卧撑的角度
        angle1 = detector.find_angle(img, 12, 24, 26)  # 躯干
        angle2 = detector.find_angle(img, 12, 14, 16)  # 手臂右
        # 进度条长度
        bar = np.interp(angle2, (45, 150), (w // 2 - 100, w // 2 + 100))
        cv2.rectangle(img, (w // 2 - 100, h - 150),
                      (int(bar), h - 100), (0, 255, 0), cv2.FILLED)
        # 角度小于50度认为撑下
        if angle2 <= 70 and angle1 >= 100 and angle1 <= 180:
            if pushdir == 0:
                pushcount = pushcount + 0.5
                dir = 1
        # 角度大于125度认为撑起
        if angle2 >= 125 and angle1 >= 100 and angle1 <= 180:
            if pushdir == 1:
                pushcount = pushcount + 0.5
                pushdir = 0
        cv2.putText(img, str(int(pushcount)), (w // 2, h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 20, cv2.LINE_AA)

    # 打开一个Image窗口显示视频图片
    cv2.imshow('Image', img)
    # cv2.waitKey(1)
