import tools
import cv2
import numpy as np


for i in range(100):
    #q quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    b_img = tools.get_sc() #cv2.cvtColor(np.array(cv2.imread('test.png')), cv2.COLOR_RGBA2BGR)

    cir_cent = tools.find_c(b_img)

    for cent in cir_cent:
        tools.move_cc(cent)