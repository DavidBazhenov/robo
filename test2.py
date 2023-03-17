import cv2 as cv, cv2
import numpy as np
import math

def nothing(args): pass


# создаем окно для отображения результата и бегунки
cv2.namedWindow("setup")

cv2.createTrackbar("b1", "setup", 0, 255, nothing)
cv2.createTrackbar("g1", "setup", 0, 255, nothing)
cv2.createTrackbar("r1", "setup", 0, 255, nothing)
cv2.createTrackbar("b2", "setup", 255, 255, nothing)
cv2.createTrackbar("g2", "setup", 255, 255, nothing)
cv2.createTrackbar("r2", "setup", 255, 255, nothing)
cv2.createTrackbar("set", "setup", 0, 1, nothing)
cv2.setTrackbarPos("b1", "setup", 78)
cv2.setTrackbarPos("g1", "setup", 0)
cv2.setTrackbarPos("r1", "setup", 9)
cv2.setTrackbarPos("b2", "setup", 241)
cv2.setTrackbarPos("g2", "setup", 97)
cv2.setTrackbarPos("r2", "setup", 59)

if __name__ == '__main__':
    cv.namedWindow( "result" )
    cap = cv.VideoCapture(0)



    hsv_min = np.array((71, 135, 132), np.uint8)
    hsv_max = np.array((167, 168, 227), np.uint8)

    color_blue = (255,0,0)
    color_red = (0,0,128)

    while True:
        flag, img = cap.read()
        img = cv.flip(img,1)

        set = cv2.getTrackbarPos('set', 'setup')
        if set == 1:
            min_p = (20, 100, 100)
            max_p = (30, 255, 255)
        else:
            r1 = cv2.getTrackbarPos('r1', 'setup')
            g1 = cv2.getTrackbarPos('g1', 'setup')
            b1 = cv2.getTrackbarPos('b1', 'setup')
            r2 = cv2.getTrackbarPos('r2', 'setup')
            g2 = cv2.getTrackbarPos('g2', 'setup')
            b2 = cv2.getTrackbarPos('b2', 'setup')
            min_p = (g1, b1, r1)
            max_p = (g2, b2, r2)



        # собираем значения из бегунков в множества

        try:
            #img = cv2.equalizeHist(img)  # Применяем эквализацию гистограммы
            img_mask = cv2.inRange(img, min_p, max_p)
            img_m = cv2.bitwise_and(img, img, mask=img_mask)
            cv2.imshow('setimg', img_m)
            contours0, hierarchy = cv.findContours(img_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

            for cnt in contours0:
                rect = cv.minAreaRect(cnt)
                box = cv.boxPoints(rect)
                box = np.int0(box)
                center = (int(rect[0][0]),int(rect[0][1]))
                area = int(rect[1][0]*rect[1][1])

                edge1 = np.int0((box[1][0] - box[0][0],box[1][1] - box[0][1]))
                edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

                usedEdge = edge1
                if cv.norm(edge2) > cv.norm(edge1):
                    usedEdge = edge2

                reference = (1,0) # horizontal edge
                angle = 180.0/math.pi * math.acos((reference[0]*usedEdge[0] + reference[1]*usedEdge[1]) / (cv.norm(reference) *cv.norm(usedEdge)))

                if area > 500:
                    cv.drawContours(img,[box],0,color_blue,2)
                    cv.circle(img, center, 5, color_red, 2)
                    cv.putText(img, "%d" % int(angle), (center[0]+20, center[1]-20), cv.FONT_HERSHEY_SIMPLEX, 1, color_red, 2)
            cv.imshow('result', img)
        except:
            cap.release()
            raise
        ch = cv.waitKey(5)
        if ch == 27:
            break

    cap.release()
    cv.destroyAllWindows()