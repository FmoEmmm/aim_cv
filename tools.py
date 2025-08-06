import cv2
import mss
import numpy as np
import pydirectinput
import time
import math

# PID
KP = 0.09
KI = 0.0
KD = 0.45
# PID状态
last_error_x = 0
last_error_y = 0
integral_x = 0
integral_y = 0

#屏幕捕获
def get_scrm():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)# RGBA 格式
        img = np.array(sct_img)# 转换NumPy 
        scimg = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)# 转换BGR
        return scimg


def find_edg(scimg):
    #蓝色的颜色范围 HSV,返回轮廓列表
    hsv = cv2.cvtColor(scimg, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([82, 199, 118])  # 蓝色下限
    upper_blue = np.array([97, 255, 255]) # 蓝色上限
    
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours

def get_mous():
    # pydirectinput 获取当前鼠标位置
    return pydirectinput.position()

def find_ccent(contours, mouse_pos):
    
    closest_center = (-1, -1)
    min_distance = float('inf')
    
    for contour in contours:
        
        rect = cv2.boundingRect(contour)
        center = (rect[0] + rect[2] // 2, rect[1] + rect[3] // 2)
        
        distance = math.sqrt((center[0] - mouse_pos[0])**2 + (center[1] - mouse_pos[1])**2)
        
        if distance < min_distance:
            min_distance = distance
            closest_center = center
            
    return closest_center

def move_cc(contour_center, speed=0.1):
    
    global last_error_x, last_error_y, integral_x, integral_y
    
    target_x, target_y = contour_center
    current_x, current_y = pydirectinput.position()

    # PID 控制器计算
    error_x = target_x - current_x
    error_y = target_y - current_y

    integral_x += error_x
    integral_y += error_y
    
    # 比例项、积分项和微分项
    p_term_x = KP * error_x
    p_term_y = KP * error_y
    
    # 计算新的鼠标位置
    new_x = int(current_x + p_term_x)
    new_y = int(current_y + p_term_y)
    
    # 移动鼠标
    pydirectinput.moveTo(new_x, new_y)
    
    # 更新误差
    last_error_x = error_x
    last_error_y = error_y
    
    distance = math.sqrt(error_x**2 + error_y**2)
    
    # 如果鼠标距离目标足够近，执行点击
    if distance < 36:
        pydirectinput.click(new_x, new_y)
        time.sleep(speed)