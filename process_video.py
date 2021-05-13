# create a folder to store extracted images
import os
folder = 'source_folder/'
if not os.path.exists(folder):
    os.mkdir(folder)
# use opencv to do the job
import cv2
vidcap = cv2.VideoCapture('panorama.mp4')
count = 0
while True:
    print(f"Processing: {count}")
    success,image = vidcap.read()
    if not success:
        break
    cv2.imwrite(os.path.join(folder,"frame{:d}.jpg".format(count)), image)     # save frame as JPEG file
    count += 1
print("{} images are extacted in {}.".format(count,folder))