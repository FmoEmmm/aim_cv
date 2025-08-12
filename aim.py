import tools
import mous
from mous import PID
import keyboard
import time
import cv2
import math

def main():
    
    # --- 初始化 ---
    print("程序将在3秒后启动...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("按 'q' 键退出")

    speed = 0       #点击间隔
    b_size = 180    #过滤大小
    min_dsten = 13  #最小距离
    
    # 创建PID控制器实例，设置Kp、Ki、Kd参数
    pid = PID(Kp=1.0, Ki=0.001, Kd=0.022)
    
    tools.init_sct()
    #16:9
    window_width = 640
    window_height = 400
    cv2.namedWindow("screen", cv2.WINDOW_NORMAL)
    cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("screen", window_width, window_height)
    cv2.resizeWindow("mask", window_width, window_height)

    while True:
        if keyboard.is_pressed('q'):
            print("out")
            break
            
        sc_img = tools.get_scrm()
        b_img= tools.img_bule(sc_img)
        contours = tools.find_edg(b_img,sc_img,b_size)
        
        mouse_pos = mous.get_mous()
        closest_center = tools.find_ccent(contours, mouse_pos)
        

        if closest_center != (-1, -1):
            target = closest_center
            current = mouse_pos

            # 计算鼠标到目标的距离
            distance = math.sqrt((current[0] - target[0])**2 + (current[1] - target[1])**2)

            # 如果距离足够近，则左键点击，否则使用PID控制器移动鼠标
            if distance < min_dsten:
                mous.left_click()
                time.sleep(speed)
            else:
                mous.move_to(current, target, pid)
        
        # 如果找到目标，在屏幕上绘制标记
        if closest_center != (-1, -1):
            cv2.circle(sc_img, closest_center, 10, (0, 0, 255), -1)
            
        cv2.imshow("screen", sc_img)
        cv2.imshow("mask", b_img)
        
        if cv2.waitKey(1) & 0xFF == 27: # 按ESC键也可退出
            break
        
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()