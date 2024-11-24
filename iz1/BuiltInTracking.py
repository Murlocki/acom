import cv2
import struct

import numpy as np

from iz1.CamShift import CamShift
from iz1.KCFTracker import KCFTracker
from iz1.MeanShift import MeanShiftHands
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
    #Получаем разрешение видео
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Кодек видео: {struct.pack('I', fourcc).decode('utf-8')}")
    print(f"Частота кадров видео:{fps}")
    print(f"Длительность видео:{duration}s")
    print(f"Разрешение видео:{width}x{height}")
    # Инициализация трекера в зависимости от выбранного типа
    if tracker_type == 'CamShift':
        tracker = CamShift()
    elif tracker_type == 'KCF':
        tracker = KCFTracker()
    elif tracker_type == 'MedianFlow':
        tracker = MedianFlowTracker()
    elif tracker_type == "MeanShiftHands":
        tracker = MeanShiftHands()
    else:
        print("Неизвестный тип трекера")
        return
    tracker.setUpWriter(fourcc,fps,(width,height))
    tracker.process(cap,**kwargs)



# Путь к вашему видеофайлу
#video_path = 'road.mp4'
#video_path = 'cats.mp4'
#video_path = 'colorCars.mp4'
#video_path = 'duel.mp4'
video_path = 'sekiro.mp4'

# Запуск трекинга с разными методами
#Белая маска
#bottom = [np.array((0., 0.,200.))]
#top = [np.array((180.,30,255))]

#Черная маска
#bottom = [np.array([0, 0, 0])]
#top = [np.array([180, 255, 50])]

#Красная маска
#bottom = [np.array([100, 150, 50], dtype=np.uint8),np.array([140, 150, 50], dtype=np.uint8)]
#top = [np.array([140, 255, 255], dtype=np.uint8),np.array([180, 255, 255], dtype=np.uint8)]

#track_object(video_path, 'CamShift')
#track_object(video_path, 'KCF')
#track_object(video_path, 'MedianFlow')
track_object(video_path, 'MeanShiftHands')