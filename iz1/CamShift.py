from typing import Sequence

import cv2
import numpy as np


class CamShift:
    def process(self, videoCap: cv2.VideoCapture,**kwargs):
        # Читаем первый кадр
        ret, frame = videoCap.read()
        if not ret:
            print("Не удалось прочитать видео")
            return

        # Выбор области интереса (ROI)
        bbox = cv2.selectROI("Tracking", frame, False)
        roi = frame[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2])]
        roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(roi_hsv, kwargs['bottom'], kwargs['top'])
        roi_hist = cv2.calcHist([roi_hsv], [0, 1], mask, [180, 256], [0, 180, 0, 256])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

        # Установка критериев завершения
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
        while True:
            ret, frame = videoCap.read()
            if not ret:
                break

            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Вычисление обратной проекции
            backproj = cv2.calcBackProject([frame_hsv], [0], roi_hist, [0, 180], 1)

            # Применение CamShift для получения нового положения
            ret, bbox = cv2.CamShift(backproj, bbox, term_crit)

            # Рисование нового положения на кадре
            pts = cv2.boxPoints(ret)
            pts = np.int0(pts)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

            cv2.imshow("Tracking", frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        videoCap.release()
        cv2.destroyAllWindows()