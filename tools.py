import cv2
import mss
import numpy as np
import time
import math
import ctypes
import win32api
import win32gui

# PID
KP = 0.1  # 调整比例增益，增加移动速度
KI = 0.0
KD = 0.45 # 调整微分增益，抑制振荡
# PID状态
last_error_x = 0
last_error_y = 0
integral_x = 0
integral_y = 0

# 加载DLL文件
try:
    dll = ctypes.CDLL(r'.\MouseControl.dll')
    print("MouseControl.dll loaded successfully.")
    
    # 相对移动
    move_R = dll.move_R
    move_R.argtypes = [ctypes.c_int, ctypes.c_int]
    move_R.restype = None
    
    # 左键按下
    click_Left_down = dll.click_Left_down
    click_Left_down.argtypes = []
    click_Left_down.restype = None
    
    # 左键松开
    click_Left_up = dll.click_Left_up
    click_Left_up.argtypes = []
    click_Left_up.restype = None
    
except FileNotFoundError:
    print("Error: MouseControl.dll not found. Please ensure it's in the same directory.")
    dll = None
except AttributeError as e:
    print(f"Error: Could not find required functions in the DLL. Error details: {e}")
    dll = None

def get_win():
    try:
        # Aim Lab的窗口标题
        window_name = "aimlab_tb" 
        hwnd = win32gui.FindWindow(None, window_name)
        if hwnd:
            rect = win32gui.GetWindowRect(hwnd)
            return {"left": rect[0], "top": rect[1], "width": rect[2] - rect[0], "height": rect[3] - rect[1]}
        return None
    except Exception as e:
        print(f"Error getting window rectangle: {e}")
        return None

def get_scrm(window_rect):
    if not window_rect:
        return None
    with mss.mss() as sct:
        monitor = {
            "top": window_rect["top"],
            "left": window_rect["left"],
            "width": window_rect["width"],
            "height": window_rect["height"]
        }
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        scimg = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        return scimg

def find_edg(scimg):
    hsv = cv2.cvtColor(scimg, cv2.COLOR_BGR2HSV)
    # 根据游戏中小球的颜色微调HSV阈值
    lower_blue = np.array([82, 199, 118])
    upper_blue = np.array([97, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_mous():
    return win32api.GetCursorPos()

def find_ccent(contours, mouse_pos, window_rect):
    closest_center = (-1, -1)
    min_distance = float('inf')
    for contour in contours:
        rect = cv2.boundingRect(contour)
        # 将轮廓中心坐标从窗口相对坐标转换为屏幕绝对坐标
        center_x = rect[0] + rect[2] // 2 + window_rect["left"]
        center_y = rect[1] + rect[3] // 2 + window_rect["top"]
        
        distance = math.sqrt((center_x - mouse_pos[0])**2 + (center_y - mouse_pos[1])**2)
        if distance < min_distance:
            min_distance = distance
            closest_center = (center_x, center_y)
    return closest_center

def move_cc(contour_center, speed=0.1):
    global last_error_x, last_error_y, integral_x, integral_y
    if not dll:
        print("DLL not loaded, skipping mouse movement.")
        return
        
    target_x, target_y = contour_center
    current_x, current_y = get_mous()

    # PID 控制器计算
    error_x = target_x - current_x
    error_y = target_y - current_y
    integral_x += error_x
    integral_y += error_y

    p_term_x = KP * error_x
    i_term_x = KI * integral_x
    d_term_x = KD * (error_x - last_error_x)

    p_term_y = KP * error_y
    i_term_y = KI * integral_y
    d_term_y = KD * (error_y - last_error_y)

    # 计算相对移动距离
    dx = int(p_term_x + i_term_x + d_term_x)
    dy = int(p_term_y + i_term_y + d_term_y)

    try:
        move_R(dx, dy)
    except Exception as e:
        print(f"Error calling DLL move_R function: {e}")
        
    last_error_x = error_x
    last_error_y = error_y

    distance = math.sqrt(error_x**2 + error_y**2)
    if distance < 36:
        try:
            click_Left_down()
            time.sleep(0.01)
            click_Left_up()
        except Exception as e:
            print(f"Error calling DLL click functions: {e}")
        time.sleep(speed)