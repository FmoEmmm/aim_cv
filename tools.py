import cv2
import mss
import numpy as np
import math

sct = None

def init_sct():
    """初始化mss对象。"""
    global sct
    sct = mss.mss()

def get_scrm():
    """使用已初始化的sct对象进行截图。"""
    if sct is None:
        init_sct()

    monitor = sct.monitors[1] 
    sct_img = sct.grab(monitor)
    img = np.array(sct_img)
    
    return img

def img_bule(scimg):
    # 将图像从BGR颜色空间转换为HSV颜色空间
    hsv = cv2.cvtColor(scimg, cv2.COLOR_BGR2HSV)
    # 定义蓝色的HSV阈值
    lower_blue = np.array([82, 199, 118])#蓝色下界
    upper_blue = np.array([97, 255, 255])#蓝色上界
    # 根据阈值创建掩膜
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    return mask

def find_edg(mask,scimg,b_size = 200):
    # 在掩膜中查找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < b_size:  # 过滤掉面积太小的目标
            continue
            
        x, y, w, h = cv2.boundingRect(contour)
        filtered_contours.append(contour)
        cv2.rectangle(scimg, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    return filtered_contours

def find_ccent(contours, mouse_pos):
    """找到距离鼠标最近的目标中心点"""
    closest_center = (-1, -1)
    min_distance = float('inf')
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        center = (x + w // 2, y + h // 2)

        distance = math.sqrt((center[0] - mouse_pos[0])**2 + (center[1] - mouse_pos[1])**2)
        
        if distance < min_distance:
            min_distance = distance
            closest_center = center
        
    return closest_center
