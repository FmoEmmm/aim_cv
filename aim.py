import tools
import cv2
import numpy as np
import keyboard

i = 10  #循环次数
speed = 0.1#点击间隔


while True:
    #q quit
    i-=1
    if keyboard.is_pressed('q') or i == 0:
        break
    print('剩余次数：',i)
    
    b_img = tools.get_sc() #cv2.cvtColor(np.array(cv2.imread('test.png')), cv2.COLOR_RGBA2BGR)

    cir_cent = tools.find_c(b_img)

    for cent in cir_cent:
        tools.move_cc(cent,speed)

