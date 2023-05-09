import cv2

from camera import Camera


class App:

    def __init__(self, cam):
        self._camera = cam
        print('hi')
        while True:
            cv2.imshow('Webcam', self._camera.get_frame(Camera._blue))
            cv2.imshow('WebcamMask', self._camera.get_mask_frame(Camera._blue))

            key = cv2.waitKey(1) & 0xFF
            if key == 27 or cv2.getWindowProperty("Webcam", cv2.WND_PROP_VISIBLE) < 1 or cv2.getWindowProperty(
                    "WebcamMask", cv2.WND_PROP_VISIBLE) < 1:
                break
