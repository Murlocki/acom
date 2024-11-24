import cv2
from cv2 import VideoCapture


class MedianFlowTracker:
    def __init__(self):
        self.writer = None
    def setUpWriter(self,fourcc,fps,framesize):
        self.writer = cv2.VideoWriter("result.mp4",fourcc,fps,framesize)
    def process(self,videoCap:VideoCapture,**kwargs):
        # Чтение первого кадра
        ret, frame = videoCap.read()

        # Выбор области интереса (ROI)
        bbox = cv2.selectROI("Tracking", frame, False)

        # Инициализация MedianFlow трекера
        tracker = cv2.legacy.TrackerMedianFlow.create()
        tracker.init(frame, bbox)

        while True:
            ret, frame = videoCap.read()
            if not ret:
                break

            # Обновление позиции трекера
            success, bbox = tracker.update(frame)

            # Рисование bounding box на кадре
            if success:
                (x, y, w, h) = [int(v) for v in bbox]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow("Tracking", frame)
            self.writer.write(frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        self.writer.release()
        videoCap.release()
        cv2.destroyAllWindows()