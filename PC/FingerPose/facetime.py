import os
from random import random
from turtle import pu
import time
import pyautogui
import threading
import cv2
import mediapipe as mp
import math

from ctypes import cast, POINTER

import win32api
import win32con
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

lmList = []
lmList1 = []
i = 0
j = 0
statint = 0


def vol_tansfer(x):
    dict = {0: -65.25, 1: -56.99, 2: -51.67, 3: -47.74, 4: -44.62, 5: -42.03, 6: -39.82, 7: -37.89, 8: -36.17,
            9: -34.63, 10: -33.24,
            11: -31.96, 12: -30.78, 13: -29.68, 14: -28.66, 15: -27.7, 16: -26.8, 17: -25.95, 18: -25.15, 19: -24.38,
            20: -23.65,
            21: -22.96, 22: -22.3, 23: -21.66, 24: -21.05, 25: -20.46, 26: -19.9, 27: -19.35, 28: -18.82, 29: -18.32,
            30: -17.82,
            31: -17.35, 32: -16.88, 33: -16.44, 34: -16.0, 35: -15.58, 36: -15.16, 37: -14.76, 38: -14.37, 39: -13.99,
            40: -13.62,
            41: -13.26, 42: -12.9, 43: -12.56, 44: -12.22, 45: -11.89, 46: -11.56, 47: -11.24, 48: -10.93, 49: -10.63,
            50: -10.33,
            51: -10.04, 52: -9.75, 53: -9.47, 54: -9.19, 55: -8.92, 56: -8.65, 57: -8.39, 58: -8.13, 59: -7.88,
            60: -7.63,
            61: -7.38, 62: -7.14, 63: -6.9, 64: -6.67, 65: -6.44, 66: -6.21, 67: -5.99, 68: -5.76, 69: -5.55, 70: -5.33,
            71: -5.12, 72: -4.91, 73: -4.71, 74: -4.5, 75: -4.3, 76: -4.11, 77: -3.91, 78: -3.72, 79: -3.53, 80: -3.34,
            81: -3.15, 82: -2.97, 83: -2.79, 84: -2.61, 85: -2.43, 86: -2.26, 87: -2.09, 88: -1.91, 89: -1.75,
            90: -1.58,
            91: -1.41, 92: -1.25, 93: -1.09, 94: -0.93, 95: -0.77, 96: -0.61, 97: -0.46, 98: -0.3, 99: -0.15, 100: 0.0}
    return dict[x]


def voice(result):
    div = 0
    for handlms in result.multi_hand_landmarks:
        draw.draw_landmarks(img, handlms, mp.solutions.hands.HAND_CONNECTIONS, handlmsstyle, handconstyle)
        for index, lm in enumerate(handlms.landmark):

            h, w, c = img.shape  # 分别存放图像长\宽\通道数

            cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * h)  # 比例坐标x乘以宽度得像素坐标

            # （3）分别处理拇指"4"和食指"8"的像素坐标
            if index == 4:
                x1, y1, = cx, cy
            if index == 8:
                x2, y2 = cx, cy

        cv2.circle(img, (x1, y1), 12, (255, 0, 0), cv2.FILLED)

        cv2.circle(img, (x2, y2), 12, (255, 0, 0), cv2.FILLED)

        # 在拇指和食指中间画一条线段，img画板，起点和终点坐标，颜色，线条宽度
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # 拇指和食指的中点，像素坐标是整数要用//
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # 在中点画一个圈
        cv2.circle(img, (cx, cy), 12, (255, 0, 0), cv2.FILLED)

        lmList.append(math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)))

        global i, statint

        i += 1

        if i == 10:
            data1 = max(lmList)
            average = sum(lmList) / 10
            if data1 > statint:
                statint = data1
            div = (average / statint) * 100

            try:
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                temp = vol_tansfer(int(div)) * 96 / 65.25
                volume.SetMasterVolumeLevel(temp, None)
            except:
                pass

            while i > 0:
                lmList.pop()
                i -= 1


def capture(result):
    for handlms in result.multi_hand_landmarks:
        draw.draw_landmarks(img, handlms, mp.solutions.hands.HAND_CONNECTIONS, handlmsstyle, handconstyle)
        for index, lm in enumerate(handlms.landmark):

            h, w, c = img.shape  # 分别存放图像长\宽\通道数

            cx, cy = int(lm.x * w), int(lm.y * h)  # 比例坐标x乘以宽度得像素坐标

            if index == 12:
                x11, y11 = cx, cy
            if index == 16:
                x12, y12 = cx, cy
            if index == 20:
                x13, y13 = cx, cy
            if index == 9:
                x21, y21 = cx, cy
            if index == 13:
                x22, y22 = cx, cy
            if index == 17:
                x23, y23 = cx, cy
        global j

        if y11 - y21 > 0 and y12 - y22 > 0 and y13 - y23 > 0:
            j += 1
        lmList1.append((x11, x12, x13))
        if j == 5:
            x = random()
            pyautogui.screenshot('my_screenshot' + str(x) + '.png')
            j = 0


def vector_2d_angle(v1, v2):
    '''
        求解二维向量的角度
    '''
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos(
            (v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
    except:
        angle_ = 65535.
    if angle_ > 180.:
        angle_ = 65535.
    return angle_


def hand_angle(hand_):
    '''
        获取对应手相关向量的二维角度,根据角度确定手势
    '''
    angle_list = []
    # ---------------------------- thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1]))),
        ((int(hand_[3][0]) - int(hand_[4][0])), (int(hand_[3][1]) - int(hand_[4][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[6][0])), (int(hand_[0][1]) - int(hand_[6][1]))),
        ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[10][0])), (int(hand_[0][1]) - int(hand_[10][1]))),
        ((int(hand_[11][0]) - int(hand_[12][0])), (int(hand_[11][1]) - int(hand_[12][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- ring 无名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[14][0])), (int(hand_[0][1]) - int(hand_[14][1]))),
        ((int(hand_[15][0]) - int(hand_[16][0])), (int(hand_[15][1]) - int(hand_[16][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[18][0])), (int(hand_[0][1]) - int(hand_[18][1]))),
        ((int(hand_[19][0]) - int(hand_[20][0])), (int(hand_[19][1]) - int(hand_[20][1])))
    )
    angle_list.append(angle_)
    return angle_list


def h_gesture(angle_list):
    '''
        # 二维约束的方法定义手势
        # fist five gun love one six three thumbup yeah
    '''
    thr_angle = 65.  # 手指闭合则大于这个值（大拇指除外）
    thr_angle_thumb = 53.  # 大拇指闭合则大于这个值
    thr_angle_s = 49.  # 手指张开则小于这个值
    gesture_str = "Unknown"
    if 65535. not in angle_list:
        if (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "0"
            capture(results)
            timefrzz = 80000
            while timefrzz > 0:
                timefrzz -= 1
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "1"
            timefrzz = 80000
            while timefrzz > 0:
                timefrzz -= 1
            pyautogui.hotkey('ctrl', 'shift', 'esc')

        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "2"
            timefrzz = 80000
            while timefrzz > 0:
                timefrzz -= 1
            pyautogui.hotkey('ctrl', 'right')

        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] < thr_angle_s) and (angle_list[4] > thr_angle):
            gesture_str = "3"
            timefrzz = 80000
            while timefrzz > 0:
                timefrzz -= 1
            pyautogui.hotkey('ctrl', 'left')
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
            gesture_str = "4"
            timefrzz = 80000
            while timefrzz > 0:
                timefrzz -= 1
            os.system("ipconfig")

        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
            gesture_str = "5"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
            gesture_str = "6"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "8"

        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
            gesture_str = "Pink Up"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "Thumb Up"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "Fuck"
            timefrzz = 80000
            while timefrzz > 0:
                timefrzz -= 1
            win32api.MessageBox(0, "注意礼貌", "提醒", win32con.MB_OK)
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
            gesture_str = "Princess"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "Bye"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
            gesture_str = "Spider-Man"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
            gesture_str = "Rock'n'Roll"

    return gesture_str


def PoseChose(results):
    for hand_label in results.multi_handedness:
        hand_jugg = str(hand_label).split('"')[1]
        # cv2.putText(img, hand_jugg, (50, 200), 0, 1.3, (0, 0, 255), 2)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            hand_local = []
            for i in range(21):
                x = hand_landmarks.landmark[i].x * img.shape[1]
                y = hand_landmarks.landmark[i].y * img.shape[0]
                hand_local.append((x, y))
            if hand_local:
                angle_list = hand_angle(hand_local)
                gesture_str = h_gesture(angle_list)
                # cv2.putText(img, gesture_str, (50, 100), 0, 1.3, (0, 0, 255), 2)


def PoseMain(decimg):
    global img, mp_drawing, draw, mp_hands, handlmsstyle, handconstyle, results
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    draw = mp.solutions.drawing_utils
    handlmsstyle = draw.DrawingSpec(color=(0, 0, 255), thickness=5)
    handconstyle = draw.DrawingSpec(color=(0, 255, 0), thickness=5)
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75)
    img = decimg
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.flip(img, 1)
    results = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    if results.multi_handedness:
        if len(results.multi_handedness) == 1:
            label = results.multi_handedness[0].classification[0].label
            if label == 'Left':
                thread1 = threading.Thread(target=capture(results))
                thread1.start()
                thread1.join()
                thread3 = threading.Thread(target=PoseChose(results))
                thread3.start()
                thread3.join()
            elif label == 'Right':
                thread2 = threading.Thread(target=voice(results))
                thread2.start()
                thread2.join()
    cv2.namedWindow("MediaPipe Hands", 0)
    cv2.resizeWindow("MediaPipe Hands", 1600, 900)  # 设置窗口大小
    cv2.imshow('MediaPipe Hands', img)
