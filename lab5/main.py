import math

import cv2
import numpy
import numpy as np
import math

def processVideo(path,pathOutput,deltaThresh=60,countourArea=1000,kernelSize = 11,sigmaX=70,sigmaY=70):
    cap = cv2.VideoCapture(path)
    ret, frame = cap.read()
    if ret:
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gaussFrame = cv2.GaussianBlur(grayFrame, (kernelSize, kernelSize), sigmaX=sigmaX, sigmaY=sigmaY)
        img = gaussFrame
        #img = cv2.resize(gaussFrame,(sizeX,sizeY))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        videoWriter = cv2.VideoWriter(pathOutput, fourcc, 144,(w,h))
        print(videoWriter)
        while True:
            oldFrame = img.copy()
            ret, frame = cap.read()
            if not ret:
                break
            grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            gaussFrame = cv2.GaussianBlur(grayFrame,(kernelSize,kernelSize),sigmaX=sigmaX,sigmaY=sigmaY)
            #img = cv2.resize(gaussFrame,(sizeX,sizeY))
            img = gaussFrame
            #Находим разницу между фреймами
            diffFrame = cv2.absdiff(oldFrame,img)

            # Проводим двоичное разделение
            # бинаризируем её превращая пиксели, превышающие порог delta_tresh, в белый цвет, а остальные в черный
            # сохраняем только пороговое значение
            threshFrame = cv2.threshold(diffFrame, deltaThresh, 255, cv2.THRESH_BINARY)[1]

            #Находим контуры объектов
            (contours, hierarchy) = cv2.findContours(threshFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contr in contours:
                area = cv2.contourArea(contr)
                if area < countourArea:
                    continue
                videoWriter.write(frame)
                cv2.imshow('frame', threshFrame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        cap.release()
        videoWriter.release()
        cv2.destroyAllWindows()



#processVideo('ЛР4_main_video.mov')
processVideo('ЛР4_motions.mov','output.mp4')
processVideo('ЛР4_motions.mov','output1.mp4',kernelSize=3,sigmaX=50,sigmaY=50,deltaThresh=60)
processVideo('ЛР4_motions.mov','output2.mp4',kernelSize=5,sigmaX=50,sigmaY=50,deltaThresh=20)