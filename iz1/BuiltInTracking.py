import cv2
import struct

import numpy as np

from iz1.CamShift import CamShift
from iz1.KCFTracker import KCFTracker
from iz1.MedianFlow import MedianFlowTracker


# Функция для трекинга объектов
def track_object(video_path, tracker_type,**kwargs):
    # Открываем видеофайл
    cap = cv2.VideoCapture(video_path)
    # Получаем кодек
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    # Получаем частоту кадров
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Получаем общую длительность видео
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    print(f"Кодек видео: {struct.pack('I', fourcc).decode('utf-8')}")
    print(f"Частота кадров видео:{fps}")
    print(f"Длительность видео:{duration}s")

    # Инициализация трекера в зависимости от выбранного типа
    if tracker_type == 'CamShift':
        tracker = CamShift()
    elif tracker_type == 'KCF':
        tracker = KCFTracker()
    elif tracker_type == 'MedianFlow':
        tracker = MedianFlowTracker()
    else:
        print("Неизвестный тип трекера")
        return

    tracker.process(cap,**kwargs)



# Путь к вашему видеофайлу
video_path = 'ex1.mp4'

# Запуск трекинга с разными методами
#track_object(video_path, 'KCF')
#track_object(video_path, 'CamShift',bottom = np.array((0., 60.,32.)),top = np.array((180.,255.,255.)))
track_object(video_path, 'MedianFlow')