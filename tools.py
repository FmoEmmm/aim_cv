import cv2
import mss
import numpy as np
import pyautogui
import time

def get_sc():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # 假设是主显示器

        # 捕获屏幕
        sct_img = sct.grab(monitor)# RGBA 格式

        # 转换NumPy 
        img = np.array(sct_img)

        # 转换BGR
        scimg = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        return scimg


def find_c(scimg):
    #蓝色的颜色范围 HSV
    hsv = cv2.cvtColor(scimg, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([189, 92, 66])  # 蓝色下限
    upper_blue = np.array([180, 80, 100]) # 蓝色上限

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours

def move_cc(contour,speed = 0.1):
    (x, y), radius = cv2.minEnclosingCircle(contour)  
    
    area_ratio = cv2.contourArea(contour) / (np.pi * radius**2)
    if 0.7 < area_ratio < 1.1:             
        
        center_x = int(x)
        center_y = int(y)
        
        pyautogui.moveTo(center_x, center_y, duration=0.2)
        pyautogui.click()
        
        time.sleep(speed) 
