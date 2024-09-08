import cv2

formats = ['jpeg','bmp','png']
windowFlags = {cv2.WND_PROP_AUTOSIZE :cv2.WINDOW_AUTOSIZE,cv2.WND_PROP_ASPECT_RATIO:cv2.WINDOW_KEEPRATIO,cv2.WND_PROP_FULLSCREEN:cv2.WINDOW_FULLSCREEN}
imageReadFlags = [cv2.IMREAD_GRAYSCALE,cv2.IMREAD_REDUCED_COLOR_4,cv2.IMREAD_UNCHANGED   ]

for format in formats:
    for imageReadFlag in imageReadFlags:
        img = cv2.imread(f'img.{format}',imageReadFlag)
        cv2.namedWindow(f'window_autosize_{format}_{imageReadFlag}',cv2.WINDOW_AUTOSIZE)
        cv2.imshow(f'window_autosize_{format}_{imageReadFlag}', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # cv2.setWindowProperty("Display window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.namedWindow(f'window_normal_{format}_{imageReadFlag}', cv2.WINDOW_NORMAL)
        cv2.imshow(f'window_normal_{format}_{imageReadFlag}', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.namedWindow(f'window_full_{format}_{imageReadFlag}', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(f'window_full_{format}_{imageReadFlag}',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow(f'window_full_{format}_{imageReadFlag}', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

