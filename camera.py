import cv2
import numpy


class Camera:
    _lower_blue = numpy.array([100, 50, 50])
    _upper_blue = numpy.array([130, 255, 255])
    _lower_red = numpy.array([161, 155, 84])
    _upper_red = numpy.array([179, 255, 255])
    _lower_green = numpy.array([100, 50, 50])
    _upper_green = numpy.array([130, 255, 255])
    _red = "red"
    _green = "green"
    _blue = "blue"
    _min_distance = 100
    _colors = {
        _red: [_lower_red, _upper_red, (0, 0, 255)],
        _green: [_lower_green, _upper_green, (0, 255, 0)],
        _blue: [_lower_blue, _upper_blue, (255, 0, 0)],
    }

    def __init__(self):
        self._cap = cv2.VideoCapture(0)
        self._prev_frame = None
        self._prev_pos = None
        self._canvas = None

    def get_mask(self, frame, color):
        if Camera._colors.get(color) is None:
            return None
        else:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, Camera._colors.get(color)[0], Camera._colors.get(color)[1])
            kernel = numpy.ones((5, 5), numpy.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            return mask

    def get_frame(self, color):
        ret, frame = self._cap.read()
        mask = self.get_mask(frame, color)
        return self.get_frame_with_contours(mask, frame, color)

    def get_mask_frame(self, color):
        ret, frame = self._cap.read()
        return self.get_mask(frame, color)

    def get_frame_with_contours(self, mask, frame, color):
        if Camera._colors.get(color) is None:
            return None
        elif color == Camera._red:
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for i, contour in enumerate(contours):
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), Camera._colors.get(color)[2], 2)
                for j, contour2 in enumerate(contours):
                    if i != j:
                        x2, y2, w2, h2 = cv2.boundingRect(contour2)
                        distance = numpy.sqrt((x - x2) ** 2 + (y - y2) ** 2)
                        if distance < Camera._min_distance:
                            frame = cv2.resize(frame, None, fx=2 * distance / Camera._min_distance,
                                               fy=2 * distance / Camera._min_distance, interpolation=cv2.INTER_LINEAR)
                            break
            return frame
        elif color == Camera._blue:
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                max_contour = max(contours, key=cv2.contourArea)
                M = cv2.moments(max_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    current_pos = (cx, cy)
                if self._prev_pos is not None and current_pos is not None:
                    cv2.line(self._canvas, self._prev_pos, current_pos, Camera._colors.get(color)[2], 5)
                self._prev_pos = current_pos
                if self._canvas is None or self._canvas.shape[:2] != frame.shape[:2]:
                    canvas = numpy.zeros_like(frame)
                frame = cv2.add(frame, canvas)
            return frame
        else:
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in contours:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), Camera._colors.get(color)[2], 2)

            return frame

    def __del__(self):
        self._cap.release()
