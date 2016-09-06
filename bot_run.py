import conf
import telebot
import os
import shutil
from random import randrange
import time


bot = telebot.TeleBot(conf.token)

def get_file():
    tmp_filename=''
    img_path=''
    number_of_files = len(os.listdir(conf.imgDir))
    print(number_of_files)
    if (number_of_files > 1 and number_of_files <= 5):
        img_path = conf.imgDir
        while (os.path.isdir(img_path) == True):
            current_file_index = randrange(0, number_of_files) #индекс файла выбираем случайно из диапазона от 0 до количества файла
            file_list = os.listdir(conf.imgDir) #получаем список файлов из папки с изображениями
            tmp_filename = file_list[current_file_index] #получаем имя файла для рандомного индекса
            img_path = conf.imgDir + "/" + tmp_filename #получаем полный путь для файла
        number_of_images = number_of_files - 1 #получаем количество файлов в папке.тк там есть папка
        alarm_string = "Осталосось изображений: " + str(number_of_images)
        bot.send_message(conf.channel_alarm_name, alarm_string)
        img_available = True
    elif (number_of_files == 1):
        bot.send_message(conf.channel_alarm_name, "Не осталось карточек!")
        img_available = False
        tmp_filename = ''
        img_path=''
    else:
        img_path = conf.imgDir
        while (os.path.isdir(img_path) == True):
            current_file_index = randrange(0, number_of_files)  # индекс файла выбираем случайно из диапазона от 0 до количества файла
            file_list = os.listdir(conf.imgDir)  # получаем список файлов из папки с изображениями
            tmp_filename = file_list[current_file_index]  # получаем имя файла для рандомного индекса
            img_path = conf.imgDir + "/" + tmp_filename  # получаем полный путь для файла
        img_available = True
    return [img_available,
            tmp_filename,
            img_path]

def post_to_channel(img_full_path):
    photo = open(img_full_path, 'rb')
    bot.send_photo(conf.channel_name, photo)

def move_file_to_sent(img_full_path):
    shutil.move(img_full_path, conf.sentImgDir)

def main():
    gf = get_file()
    if (gf[0] == True):
        image_file = gf[2]
        print("img path: ", image_file)
        post_to_channel(image_file)
        time.sleep(2)
        move_file_to_sent(image_file)
        time.sleep(2)
    elif(gf[0]==False):
        print("There is no files there:(")
        time.sleep(1)


if __name__ == '__main__':
   main()
   time.sleep(1)