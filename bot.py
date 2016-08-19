import conf
import telebot
import os
import shutil
from random import randrange
import time
import schedule


bot = telebot.TeleBot(conf.token)

def get_file():
    number_of_files = len(os.listdir(conf.imgDir))
    img_path = conf.imgDir
    while (os.path.isdir(img_path) == True):
        current_file_index = randrange(0,number_of_files) #индекс файла выбираем случайно из диапазона от 0 до количества файла
        file_list = os.listdir(conf.imgDir) #получаем список файлов из папки с изображениями
        tmp_filename = file_list[current_file_index] #получаем имя файла для рандомного индекса
        img_path = conf.imgDir + "/" + tmp_filename #получаем полный путь для файла
    return [tmp_filename, img_path]


def post_to_channel(img_full_path):
    photo = open(img_full_path, 'rb')
    bot.send_photo(conf.channel_name, photo)

def move_file_to_sent(img_full_path):
    number_of_files = len(os.listdir(conf.imgDir))
    if (number_of_files > 2):
        shutil.move(img_full_path, conf.sentImgDir)
        return "moved"
    else:
        return "one file left"

def main():
    gf = get_file()
    image_file = gf[1]
    print("img path", image_file)
    post_to_channel(image_file)
    time.sleep(2)
    move_file_to_sent(image_file)
    time.sleep(2)

schedule.every(2).hours.do(main)
#   schedule.every(2).minutes.do(main)

if __name__ == '__main__':
    while 1:
        schedule.run_pending()
        time.sleep(1)