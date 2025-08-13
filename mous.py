import numpy as np
import time
import ctypes


user32 = ctypes.windll.user32

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

dll = None

class PID:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.last_error_x = 0
        self.last_error_y = 0
        self.integral_x = 0
        self.integral_y = 0

    def update(self, current_pos, target_pos):

        error_x = target_pos[0] - current_pos[0]
        error_y = target_pos[1] - current_pos[1]
        
        # 比例项
        p_term_x = self.Kp * error_x
        p_term_y = self.Kp * error_y

        self.integral_x += error_x
        self.integral_y += error_y
        i_term_x = self.Ki * self.integral_x
        i_term_y = self.Ki * self.integral_y

        # 微分项
        d_term_x = self.Kd * (error_x - self.last_error_x)
        d_term_y = self.Kd * (error_y - self.last_error_y)
        
        self.last_error_x = error_x
        self.last_error_y = error_y
        
        dx = int(p_term_x + i_term_x + d_term_x)
        dy = int(p_term_y + i_term_y + d_term_y)

        return dx, dy

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
    
except (AttributeError,FileNotFoundError) as e:
    print(f"Error loading MouseControl.dll: {e}")
    dll = None

def get_mous():
        class POINT(ctypes.Structure):
            _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
        
        pt = POINT()
        user32.GetCursorPos(ctypes.byref(pt))
        return (pt.x, pt.y)

def mous_mov(x,y):
    if dll:
        move_R(x,y)


def move_pid(start_pos, end_pos, pid):
    """
    使用PID控制器平滑移动鼠标到目标点。
    """
    dx, dy = pid.update(start_pos, end_pos)
    mous_mov(dx, dy)

def left_down():
        """模拟鼠标左键按下"""
        if dll:
            click_Left_down()
        else:
            user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

def left_up():
        """模拟鼠标左键抬起"""
        if dll:
            click_Left_up()
        else:
            user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def left_click():
        """模拟一次左键点击"""
        left_down()
        time.sleep(0.01) # 短暂延迟模拟点击
        left_up()
