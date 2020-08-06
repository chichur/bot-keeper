"""
код для детектирования лиц на фотографиях
"""
import cv2 as cv
import numpy as np


class Detector:
    """
    Класс детектор лиц
    """
    def __init__(self):
        self.face_cascade = cv.CascadeClassifier()
        # предтренерованная модель
        self.face_cascade.load(cv.samples.findFile('haarcascade_frontalface_default.xml'))

    # функция детектирования лиц
    def detect_face(self, file):
        npimg = np.fromstring(file, np.uint8)
        frame = cv.imdecode(npimg, cv.IMREAD_UNCHANGED)
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_gray = cv.equalizeHist(frame_gray)

        # функция возращает список прямогульников лиц
        # достаточно проверить список на заполненость
        faces = self.face_cascade.detectMultiScale(frame_gray)
        if len(faces) != 0:
            return True
        else:
            return False
