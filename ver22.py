import cv2 as cv, cv2
import numpy as np
import math
#низкая частота кадров, поскольку распознование лица происходит cо сменой каждого кадра
cap = cv.VideoCapture(0)

lower_pink = (20, 100, 100)
upper_pink = (30, 255, 255)

color_blue = (255, 0, 0)
color_red = (0, 0, 128)

while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    ret, frame = cap.read()
    #форматируем frame для передачи в декодер
    image = cv.resize(frame, (0, 0), None, 1, 1)
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    mask = cv.inRange(hsv, lower_pink, upper_pink)
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        center = (int(rect[0][0]), int(rect[0][1]))
        area = int(rect[1][0] * rect[1][1])

        edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[0][1]))
        edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

        usedEdge = edge1
        if cv.norm(edge2) > cv.norm(edge1):
            usedEdge = edge2

        reference = (1, 0)  # horizontal edge
        angle = 180.0 / math.pi * math.acos(
            (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv.norm(reference) * cv.norm(usedEdge)))

        if area > 500:
            cv.drawContours(image, [box], 0, color_blue, 2)
            cv.circle(image, center, 5, color_red, 2)
            cv.putText(image, "%d" % int(angle), (center[0] + 20, center[1] - 20), cv.FONT_HERSHEY_SIMPLEX, 1, color_red,2)
    #для frame ищем совпадения с фото из reference сравнивая функцией compare_faces
    #print(faceDis)
    cv.imshow('vid', image)