import cv2

#Get the mask of the frame for a color
def getColor(frame, lower_lim, upper_lim):
    # https://www.programcreek.com/python/example/70463/cv2.COLOR
    temp_frame = cv2.GaussianBlur(frame, (3,3), 0)
    hsv = cv2.cvtColor(temp_frame, cv2.COLOR_BGR2HSV)
    mask_color = cv2.inRange(hsv, lower_lim, upper_lim)

    return mask_color

#Return the contours of a frame
def getContours(drawFrame, frameFrom):
    rows, cols, _ = drawFrame.shape
    _, threshold = cv2.threshold(frameFrom, 25, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    return contours

#Draw the contours of a frame on the frame
def drawContours(drawFrame, frameFrom, sizeMin=30, maxSize=10000, font=cv2.FONT_HERSHEY_PLAIN):

    contours = getContours(drawFrame, frameFrom)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)

        if w < sizeMin and h < sizeMin:
            continue

        if (w * h) > maxSize:
            continue

        cv2.drawContours(drawFrame, [cnt], -3, (0, 0, 255), 3)

        cv2.rectangle(drawFrame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        x1, y1 = (x + int(w/2) - 1, y + int(h/2) - 1)
        x2, y2 = (x + int(w/2) + 1, y + int(h/2) + 1)

        cv2.rectangle(drawFrame, (x1, y1), (x2, y2), (255, 0, 238), 2)

        cv2.putText(drawFrame,"W: " + str(w) + ", H: " + str(h), (x, y - 15), font, 1, (255, 237, 43), 2, cv2.LINE_4)

    return drawFrame

