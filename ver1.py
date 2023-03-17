import cv2
# ищет розовые квадраты
image = cv2.imread('hall.jpg')
image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_pink = (140, 50, 50)
upper_pink = (180, 255, 255)

mask = cv2.inRange(hsv, lower_pink, upper_pink)
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    area = cv2.contourArea(contour)
    if area > 500:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
