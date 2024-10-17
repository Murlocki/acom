import os
dir = '../data'
print(os.listdir(dir))
images = [f for f in os.listdir(dir) if f.endswith(('.jpg', '.jpeg', '.png', '.tif', '.bmp'))]
boxes = [f for f in os.listdir(dir) if f.endswith(('box'))]
print(images)
print(boxes)
print(f"{len(images)} number of images found")
#lang = input('Enter The language without spaces\n')
#font = input('Enter font without spaces\n')
part1 = f"rus.eng.myFont.exp"
for i, image in enumerate(images):
    filename = f"{part1}{i}.{image[-3:]}"
    print(filename)
    os.rename(os.path.join(dir, image), os.path.join(dir, filename))

    filename = f"{part1}{i}.{boxes[i][-3:]}"
    print(filename)
    os.rename(os.path.join(dir, boxes[i]), os.path.join(dir, filename))
    print('///////////')