import cv2
import mss
import numpy as np
import pyautogui
import time



def get_sc():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # 假设是主显示器

        # 捕获屏幕
        sct_img = sct.grab(monitor)

        # 转换为 NumPy 数组，此时是 RGBA 格式
        img = np.array(sct_img)

        # 转换为 OpenCV 常用的 BGR 格式
        scimg = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        return scimg


def find_c(img_b):
    #蓝色的颜色范围 HSV
    hsv = cv2.cvtColor(img_b, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 150, 50])  # 蓝色下限
    upper_blue = np.array([140, 255, 255]) # 蓝色上限
            
    # 创建一个掩码，只保留蓝色区域
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
            
    # # 使用开运算去除小的噪声
    # kernel = np.ones((5, 5), np.uint8)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # 寻找图像中的所有轮廓
    # `cv2.RETR_EXTERNAL` 只寻找最外层轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours

def move_cc(contour,img_b):
    (x, y), radius = cv2.minEnclosingCircle(contour)               
            # 转换中心点坐标为整数
    center_x = int(x)
    center_y = int(y)
    # 绘制一个圆形和中心点，用于调试和可视化
    cv2.circle(img_b, (center_x, center_y), int(radius), (0, 255, 0), 2)
    cv2.circle(img_b, (center_x, center_y), 5, (0, 0, 255), -1)
    
    print(f"找到蓝色球，坐标: ({center_x}, {center_y})")
    
    # 5. 鼠标移动和点击
    pyautogui.moveTo(center_x, center_y, duration=0.2)
    pyautogui.click()
                        
    # 暂停一段时间，避免连续点击
    time.sleep(0.1) 
    
    
if __name__ == "__main__":
    pass