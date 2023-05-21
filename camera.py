import cv2
import numpy
import heapq
import datetime


class Camera:
    _lower_blue = numpy.array([100, 120, 100])
    _upper_blue = numpy.array([130, 255, 200])
    _lower_red = numpy.array([161, 155, 84])
    _upper_red = numpy.array([179, 255, 255])
    _lower_green = numpy.array([45, 50, 120])
    _upper_green = numpy.array([90, 255, 150])
    _red = "red"
    _green = "green"
    _blue = "blue"
    _min_distance = 200
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
            blur_image = cv2.medianBlur(hsv, 21)
            mask = cv2.inRange(blur_image, Camera._colors.get(color)[0], Camera._colors.get(color)[1])
            kernel = numpy.ones((3, 3), numpy.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            return mask

    def get_frame(self, color, frame=None):
        if not numpy.any(frame):
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
            return self.get_drawing_frame(mask, frame, color)
        elif color == Camera._blue:
            return self.get_zoomed_frame(mask, frame, color)
        else:
            self.colors_touched(mask, frame, color)

            return frame

    def get_zoomed_frame(self, mask, frame, color):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) >= 2:
            max_2_contours = heapq.nlargest(2, contours, key=cv2.contourArea)
            if cv2.contourArea(max_2_contours[0]) > cv2.contourArea(max_2_contours[1]) * 1.5 or cv2.contourArea(
                    max_2_contours[1]) > cv2.contourArea(max_2_contours[0]) * 1.5:
                distance = 0
            else:
                for i, contour in enumerate(max_2_contours):
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), Camera._colors.get(color)[2], 2)
                    for j, contour2 in enumerate(max_2_contours):
                        if i != j:
                            x2, y2, w2, h2 = cv2.boundingRect(contour2)
                            distance = numpy.sqrt((x - x2) ** 2 + (y - y2) ** 2)
            if distance <= Camera._min_distance:
                scale = 2 - (distance / Camera._min_distance)

                y_size = frame.shape[0]
                x_size = frame.shape[1]

                px = int(0.5 * x_size * (1 - 1 / scale))
                px2 = int(x_size - 0.5 * x_size * (1 - 1 / scale))
                py = int(0.5 * y_size * (1 - 1 / scale))
                py2 = int(y_size - 0.5 * y_size * (1 - 1 / scale))

                img_cropped = frame[py:py2, px:px2]
                frame = cv2.resize(img_cropped, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
            else:
                frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_LINEAR)
        return frame

    def capture_frame(self, frame):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'image_{timestamp}.jpg'
        cv2.imwrite(filename, frame)

    def get_drawing_frame(self, mask, frame, color):
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
                self._canvas = numpy.zeros_like(frame)
            frame = cv2.add(frame, self._canvas)
        return frame

    def get_frames(self):
        return self.get_drawing_frame(self.get_mask_frame(self._red),
                                      self.get_frame(Camera._blue, self.get_frame(Camera._green)),
                                      self._red)

    def colors_touched(self, mask, frame, color):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) >= 2:
            max_2_contours = heapq.nlargest(2, contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(max_2_contours[0])
            x2, y2, w2, h2 = cv2.boundingRect(max_2_contours[1])
            cv2.rectangle(frame, (x, y), (x + w, y + h), Camera._colors.get(color)[2], 2)
            cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), Camera._colors.get(color)[2], 2)
            distance = numpy.sqrt((x - x2) ** 2 + (y - y2) ** 2)
            if cv2.contourArea(max_2_contours[0]) > cv2.contourArea(max_2_contours[1]) * 1.5 or cv2.contourArea(
                    max_2_contours[1]) > cv2.contourArea(max_2_contours[0]) * 1.5:
                if (distance <= 50):
                    self.capture_frame(frame)
        return frame

    def __del__(self):
        self._cap.release()
