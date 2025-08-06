import tools
import keyboard
import time
import cv2
import math

def main():
    i = 100
    speed = 0.1
    
    # 定义一个阈值，用于判断小球是否足够靠近屏幕中心
    # 这个值需要根据游戏分辨率和小球大小进行调整
    click_threshold = 50 
    
    for j in range(5):
        print("start:", j)
        time.sleep(1)
    
    while True:
        if keyboard.is_pressed('q') or i == 0:
            break
        #i -= 1
        print("倒计时", i)
        
        window_rect = tools.get_win()
        if not window_rect:
            print("Aim Lab window not found, waiting...")
            time.sleep(1)
            continue
            
        b_img = tools.get_scrm(window_rect)
        if b_img is None:
            time.sleep(0.1)
            continue
        
        # 显示捕捉画面（可选）
        cv2.imshow('Capture', b_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        contours = tools.find_edg(b_img)
        mouse_pos = tools.get_mous()
        
        # 寻找距离屏幕中心最近的小球
        closest_center = tools.find_ccent(contours, mouse_pos, window_rect)
        
        if closest_center != (-1, -1):
            target_x, target_y = closest_center
            
            # 获取屏幕中心坐标
            screen_center_x = window_rect["left"] + window_rect["width"] // 2
            screen_center_y = window_rect["top"] + window_rect["height"] // 2
            
            # 计算小球与屏幕中心的距离
            distance_to_center = math.sqrt((target_x - screen_center_x)**2 + (target_y - screen_center_y)**2)
            
            # 如果小球在屏幕中心附近，直接点击
            if distance_to_center < click_threshold:
                tools.click_mouse()
            # 否则，移动鼠标到小球位置
            else:
                tools.move_mouse_to_target(closest_center)

if __name__ == "__main__":
    main()