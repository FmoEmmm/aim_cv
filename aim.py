import tools
import cv2
import numpy as np

b_img= cv2.cvtColor(np.array(cv2.imread('test.png')), cv2.COLOR_RGBA2BGR)

cc,bb = tools.find_c(b_img)

tools.move_cc(cc,bb)