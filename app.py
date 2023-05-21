import cv2

from camera import Camera


class App:

    def __init__(self, cam):
        self._camera = cam
        print('hi')
        while True:
            cv2.imshow('Webcam', self._camera.get_frames())
            cv2.imshow('Webcam', self._camera.get_mask_frame(Camera._green))

            key = cv2.waitKey(1) & 0xFF
            if key == 27 or cv2.getWindowProperty("Webcam", cv2.WND_PROP_VISIBLE) < 1:
                break
