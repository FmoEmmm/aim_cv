import tools
import keyboard
import time
import cv2  # 新增: 导入cv2库

def main():
    i = 100
    speed = 0.1
    
    for j in range(5):
        print("start:", j)
        time.sleep(1)
    
    while True:
        if keyboard.is_pressed('q'):
            break
        
        # 为了演示，可以去掉倒计时，让循环持续运行
        # i -= 1
        # print("倒计时", i)
        
        window_rect = tools.get_win()
        if not window_rect:
            print("Aim Lab window not found, waiting...")
            time.sleep(1)
            continue
            
        b_img = tools.get_scrm(window_rect)
        if b_img is None:
            time.sleep(0.1)
            continue
        
        # 新增: 显示捕捉的画面
        # 'Capture'是窗口标题
        cv2.imshow('Capture', b_img)
        
        # 新增: 等待1毫秒，如果按下'q'键，则退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        contours = tools.find_edg(b_img)
        mouse_pos = tools.get_mous()
        closest_center = tools.find_ccent(contours, mouse_pos, window_rect)
        
        if closest_center != (-1, -1):
            tools.move_cc(closest_center, speed)
    
    # 新增: 循环结束后销毁所有窗口
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()