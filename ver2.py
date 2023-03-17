import cv2 as cv, cv2
import numpy as np
import math

cap = cv.VideoCapture(0)

# вот эти настройки надо постоянно корректировать, сильно зависит от камеры, освещения, цвета маркера<-----
lower_y = (0, 0, 255)
upper_y = (182, 165, 255)

lower_b = (224, 203, 0)
upper_b = (255, 255, 231)
# вот эти настройки надо постоянно корректировать, сильно зависит от камеры, освещения, цвета маркера<-----

color_blue = (255, 0, 0)
color_red = (0, 0, 128)


screen = np.zeros((480, 640, 3), dtype=np.uint8)
while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    #форматируем frame для передачи в декодер
    image = cv.resize(frame, (0, 0), None, 1, 1)
    mask_y = cv.inRange(image, lower_y, upper_y)
    mask_b = cv.inRange(image, lower_b, upper_b)
    contours_y, _ = cv.findContours(mask_y, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours_b, _ = cv.findContours(mask_b, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    for cnt in contours_y:
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        boxe = np.int0(box)
        center = (int(rect[0][0]), int(rect[0][1]))
        area = int(rect[1][0] * rect[1][1])
        if area > 500:
            for cnt_b in contours_b:
                rect_b = cv.minAreaRect(cnt_b)
                center_b = (int(rect_b[0][0]), int(rect_b[0][1]))
                if abs(center[0] - center_b[0]) <= 50 and abs(center[1] - center_b[1]) <= 50 and center_b[0] > 0 \
                        and center_b[1] > 0 and center_b[0] < 640 and center_b[1] < 480:
                    screen = np.zeros((480, 640, 3), dtype=np.uint8)
                    cv2.circle(screen, (320, 480), 5, (255, 255, 0), -1)
                    print("-->  ", center_b[0], center_b[1])
                    a = 320 - center_b[0]
                    b = 480 - center_b[1]
                    c = math.sqrt(a**2 + b**2)
                    cos = b/c
                    degree = math.degrees(math.asin(cos))
                    if center_b[0] < 320:
                        degree = 180 - degree
                    cv2.putText(screen, 'Sin: '+str(cos), (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                        1, (255, 0, 0), 2, cv2.LINE_AA)
                    cv2.putText(screen, 'Deg: ' + str(degree), (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (255, 0, 0), 2, cv2.LINE_AA)
                    print("==================================")
                    print("heigh: ", 480 - center_b[1], "width: ", 320 - center_b[0], "c:  ", c)
                    print(f"a ->{a} b ->{b} c ->{c}")
                    print("==================================")
                    cv2.circle(screen, (center_b[0], center_b[1]), 5, (0, 255, 0), -1)
                    cv2.line(screen, (320, 480), (center_b[0], center_b[1]), (0, 255, 255), 3)
                    break
    cv2.imshow("Image", screen)
    cv2.imshow("im", image)