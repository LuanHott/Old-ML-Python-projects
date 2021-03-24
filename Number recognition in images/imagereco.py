import numpy as np
from cv2 import cv2
from mss import mss
from PIL import Image
import pytesseract as ocr
from matplotlib import pyplot as plt

ocr.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

t3 = cv2.imread('t3.png')
t4 = cv2.imread('t4.png')
t5 = cv2.imread('t5.png')
t6 = cv2.imread('t6.png')
t7 = cv2.imread('t7.png')
t8 = cv2.imread('t8.png')

template_data=[t3,t4,t5,t6,t7,t8]

img_rgb = cv2.imread('teste.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('t8.png',0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite('res.png',img_rgb)