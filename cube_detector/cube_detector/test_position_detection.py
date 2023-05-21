import cv2
import numpy as np

	
image = cv2.imread('ur_test.png')
height, width, channels = image.shape
img_size_y =  height
img_size_x = width

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


high_thresh, thresh_im = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
lowThresh = 0.5*high_thresh
edge = cv2.Canny(gray_image, 10, 350)

contours, hierarchy = cv2.findContours(edge, 
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print("Number of Contours found = " + str(len(contours)))
for cnt in contours:
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        # cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)
        # cv2.circle(image, (cx, cy), 7, (0, 0, 255), -1)
        # cv2.putText(image, "center", (cx - 20, cy - 20),
        #         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    #print(f"x: {cx} y: {cy}")
    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    x, y, w, h = cv2.boundingRect(cnt)
    ratio = float(w)/h
    if ratio >= 0.9 and ratio <= 1.1:
        print(f"x: {cx} y: {cy}")
        cv2.drawContours(image, [cnt], -1, (0, 255, 0), 1)
        cv2.circle(image, (cx, cy), 4, (0, 0, 255), -1)


        # get rotated rectangle from outer contour
        rotrect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rotrect)
        box = np.int0(box)

        # get angle from rotated rectangle
        angle = rotrect[-1]

        # from https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
        # the `cv2.minAreaRect` function returns values in the
        # range [-90, 0); as the rectangle rotates clockwise the
        # returned angle trends to 0 -- in this special case we
        # need to add 90 degrees to the angle
        if angle < -45:
            angle = -(90 + angle)
        
        # otherwise, just take the inverse of the angle to make
        # it positive
        else:
            angle = -angle

        print(angle,"deg")



cv2.imshow('Image', image)

cv2.waitKey(0)
cv2.destroyAllWindows()
