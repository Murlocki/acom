import cv2
def readIPWriteTOFile():
    cap = cv2.VideoCapture(r"video.mp4")
    ok, img = cap.read()
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter("output.mp4", fourcc,fps=10, frameSize=(w, h))
    while (True):
        current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)

        ok, img = cap.read()
        if not(ok):
            break
        cv2.imshow('img', img)
        video_writer.write(img)
        #скипнули кадры для быстрой записи
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame + 20)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()

readIPWriteTOFile()