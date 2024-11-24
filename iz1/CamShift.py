from typing import Sequence

import cv2
import numpy as np


class CamShift:

    def createMask(self,frame,low,top):
        resultMask = np.zeros_like(frame[:,:,0])
        for i in range(len(low)):
            mask = cv2.inRange(frame, low[i], top[i])
            resultMask = cv2.bitwise_or(resultMask,mask)
        return resultMask
    def __init__(self):
        self.writer = None
    def setUpWriter(self,fourcc,fps,framesize):
        self.writer = cv2.VideoWriter("result.mp4",fourcc,fps,framesize)
    def process(self, cap: cv2.VideoCapture,**kwargs):
        # Читаем первый кадр
        ret, frame = cap.read()
        if not ret:
            print("Не удалось прочитать видео")
            return

        bbox = cv2.selectROI(frame)
        (x, y, w, h) = bbox
        track_window = (x, y, w, h)
        roi = frame[y:y + h, x:x + w]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = None if(not kwargs.keys().__contains__('bottom')) else self.createMask(hsv_roi, kwargs['bottom'], kwargs['top'])
        if mask is not None and mask.size > 0: cv2.imshow('Mask', mask)

        roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        while True:
            ret, frame = cap.read()
            if ret == True:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = None if (not kwargs.keys().__contains__('bottom')) else self.createMask(hsv,kwargs['bottom'],kwargs['top'])
                if mask is not None and mask.size > 0: cv2.imshow('Mask',mask)

                dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

                cv2.imshow('BackProj',dst)

                # apply CAMShift to get the new location
                ret, track_window = cv2.CamShift(dst, track_window, term_crit)
                pts = cv2.boxPoints(ret)
                pts = np.int0(pts)
                img2 = cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
                cv2.imshow('Result', img2)
                self.writer.write(img2)
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break
            else:
                break
        self.writer.release()
        cap.release()
        cv2.destroyAllWindows()