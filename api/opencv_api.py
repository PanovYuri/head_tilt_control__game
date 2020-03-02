import numpy as np
import cv2


class OcvApi():

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

    vert_sens = 7
    horz_sens = 15

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.smile_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_smile.xml')

        self.img = cv2.VideoCapture(0)

        self.firstSet = True
        self.oldPos = [0, 0, 0, 0]
        self.is_smile = False

    def __set_ferst_pos(self, a):
        self.oldPos = a

    def get_smile(self, face, gray):
        for (x, y, w, h) in [face]:
            roi_gray = gray[y:y+h, x:x+w]
            smile = self.smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
        if len(smile) > 0:
            return True
        return False

    def get_face_pos(self):
        _, f = self.img.read()
        gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        main_face = [0, 0, 0, 0]
        self.is_smile = False
        if len(faces) != 0:
            main_face = faces[0]
            self.is_smile = self.get_smile(main_face, gray)

        max_w = main_face[2]

        for (x, y, w, h) in faces:
            if max_w < w:
                max_w = w
                main_face = [x, y, w, h]

        if self.firstSet:
            self.__set_ferst_pos(main_face)
            self.firstSet = False
        return main_face

    def get_direction(self):
        main_dir = [False, False, False, False]
        (x, y, w, h) = self.get_face_pos()

        this_x_state = self.oldPos[0] - x
        if abs(this_x_state) > w / self.vert_sens and this_x_state != 0:
            if this_x_state > 0:
                main_dir[0] = True
            else:
                main_dir[1] = True

        this_y_state = self.oldPos[1] - y
        if abs(this_y_state) > h / self.horz_sens and this_y_state != 0:
            if this_y_state > 0:
                main_dir[2] = True
            else:
                main_dir[3] = True

        return main_dir
