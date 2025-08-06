import tools
import keyboard
import time


def main():
    
    i = 100 #计时
    speed = 0.7#点击间隔
    
    for j in range(5):
        print("start:",j)
        time.sleep(1)
    
    
    while True:
        # 非阻塞式退出
        if keyboard.is_pressed('q') or i == 0:#q 退出
            break
        #i -= 1
        print("倒计时",i)
        # 捕获屏幕
        b_img = tools.get_scrm()
        
        if b_img is None:
            time.sleep(0.1)
            continue
        
        # 寻找蓝色球的轮廓
        contours = tools.find_edg(b_img)
        
        # 获取当前鼠标位置
        mouse_pos = tools.get_mous()
        
        # 找到最近的目标中心点
        closest_center = tools.find_ccent(contours, mouse_pos)
        
        # 如果找到有效目标
        if closest_center != (-1, -1):
            # 使用 PID 移动鼠标并点击
            tools.move_cc(closest_center, speed)

if __name__ == "__main__":
    main()

