from paletteList import paletteList
import numpy as np
import pdb
import cv2
import sys
from tqdm import tqdm
import math
from collections import Counter
import concurrent.futures
import os

class handle_palette(object):
    def __init__(self, image_name, palette_list):
        self.palette_list = palette_list
        self.image_name = image_name
        self.img = cv2.imread(image_name)
        self.unchanged_img = cv2.imread(image_name, cv2.IMREAD_UNCHANGED)
        self.height, self.width, self.channels = self.img.shape
        self.pixel_square_size = 2

    def convertPalette(self):
        scaled_width = math.floor(self.width/self.pixel_square_size)
        scaled_height = math.floor(self.height/self.pixel_square_size)

        for i in range(0, scaled_width):
            for j in range(0, scaled_height):
                image_square = self.img[j*self.pixel_square_size:(j+1)*self.pixel_square_size, i*self.pixel_square_size:(i+1)*self.pixel_square_size]
                image_mean_color = np.mean(image_square.reshape((-1, 3)), axis=0)
                rgb_color = self.switch_image_order(image_mean_color)
                self.unchanged_img[j*self.pixel_square_size:(j+1)*self.pixel_square_size, i*self.pixel_square_size:(i+1)*self.pixel_square_size][:, :, :3] = self.switch_image_order(self.nearby_Color(rgb_color))

    def switch_image_order(self, input_color):
        return np.asarray([input_color[2], input_color[1], input_color[0]])

    def nearby_Color(self, actualColor):
        assert len(self.palette_list) > 0
        selectedColor = [0, 0, 0]
        currentSim = sys.maxsize
        for color in self.palette_list:
            similarity = self.color_similarity(actualColor, color)
            if similarity < currentSim:
                currentSim = similarity
                selectedColor = color
        return selectedColor

    def color_similarity(self, rgbColor, compareColor):
        assert len(rgbColor) == 3
        assert len(compareColor) == 3
        return np.linalg.norm(rgbColor - compareColor)

    def show_image(self):
        cv2.imshow('img', self.unchanged_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_image(self):
        if not os.path.exists("target_folder"):
            os.mkdir("target_folder")
        cv2.imwrite(f"./target_folder/{self.image_name.split('/')[-1]}", self.unchanged_img)

def single_processor(i):
    HP = handle_palette(f"./source_folder/frame{i}.jpg", paletteList[5])
    HP.convertPalette()
    HP.show_image()
    pdb.set_trace()
    HP.save_image()
    if i % 100 == 0:
        print(f"finish {i}")

def noise_filter(window_size = 3, pixel_square_size = 4, max_size = 100):
    if not os.path.exists("filtered_folder"):
        os.mkdir("filtered_folder")
    def get_single_img_square(img, j, i):
        'find the square value of one img at given place'
        image_square = img[j * pixel_square_size:(j + 1) * pixel_square_size,
                       i * pixel_square_size:(i + 1) * pixel_square_size]
        return (image_square[0][0][0], image_square[0][0][1], image_square[0][0][2])

    print("reading images...")
    img_array = []
    for i in tqdm(range(max_size)):
        img = cv2.imread(f"./target_folder/frame{i}.jpg")
        img_array.append(img)

    print("post processing images...")
    height, width, _ = img.shape
    scaled_width = math.floor(width / pixel_square_size)
    scaled_height = math.floor(height / pixel_square_size)
    for img_index in tqdm(range(max_size)):
        # get sequences before and after current image
        half_window = window_size//2
        current_img_array = img_array[max(0, img_index-half_window):min(max_size, img_index+half_window)]
        for i in range(0, scaled_width):
            for j in range(0, scaled_height):
                mode_list = []
                for sig_img in current_img_array:
                    mode_list.append(get_single_img_square(sig_img, j, i))
                # Use the mode of past arries
                img[j * pixel_square_size:(j + 1) * pixel_square_size, i * pixel_square_size:(i + 1) * pixel_square_size] = Counter(mode_list).most_common(1)[0][0]
        cv2.imwrite(f"./filtered_folder/frame{img_index}.jpg", img)

def merge_into_video(max_size):
    print("Merging images into video")
    img_array = []
    for i in tqdm(range(max_size)):
        img = cv2.imread(f"./filtered_folder/frame{i}.jpg")
        img_array.append(img)
    out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, (1280, 720))
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

if __name__ == '__main__':
    # max_size = 6667
    # print("Transferring images...")
    # executor = concurrent.futures.ProcessPoolExecutor(1)
    # futures = [executor.submit(single_processor, i) for
    #            i in range(max_size)]
    # concurrent.futures.wait(futures)
    # noise_filter(max_size=max_size)
    # merge_into_video(max_size=max_size)

    HP = handle_palette(f"test42.png", paletteList[5])
    HP.convertPalette()
    # HP.show_image()
    cv2.imwrite("res.png", HP.unchanged_img)



