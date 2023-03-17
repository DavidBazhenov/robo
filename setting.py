import numpy as np
import cv2

def nothing(args):pass
cv2.namedWindow("setup")
cv2.namedWindow("setup2")
cv2.createTrackbar("b1", "setup", 0, 255, nothing)
cv2.createTrackbar("g1", "setup", 0, 255, nothing)
cv2.createTrackbar("r1", "setup", 0, 255, nothing)
cv2.createTrackbar("b2", "setup", 255, 255, nothing)
cv2.createTrackbar("g2", "setup", 255, 255, nothing)
cv2.createTrackbar("r2", "setup", 255, 255, nothing)
cv2.createTrackbar("blur", "setup2", 0, 10, nothing)
fn = "hall.jpg" # путь к файлу с картинкой
img = cv2.imread(fn) # загрузка изображения
percent = 50
width = int(img.shape[1] * percent / 100)
height = int(img.shape[0] * percent / 100)
dim = (width, height)
img = cv2.resize(img, dim)
while True:
    min_p = np.array([20, 100, 100])
    max_p = np.array([30, 255, 255])
    img_mask = cv2.inRange(img, min_p, max_p)
    img_m = cv2.bitwise_and(img, img, mask = img_mask)
    cv2.imshow('img', img_m)
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()