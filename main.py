import config
import telebot
import os
from shutil import move
from random import randrange
import datetime
import logging

bot = telebot.TeleBot(config.telegram_token)
logging.basicConfig(format = u'%(filename) s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level = logging.ERROR, filename="bot.log")

def get_img_list(folder='./'):
    _filelist=[]
    filelist = os.listdir(folder)
    for i in range(len(filelist)):
      if (os.path.isfile(folder+'/'+filelist[i]) == True):
            _filelist.append(filelist[i])
    return _filelist

def get_random_file(filelist, folder='./', ):
    filenum = randrange(0, len(filelist))
    filepath = folder + '/' + filelist[filenum]
    return filepath

def check_file_count(list):
    if len(list) <= 5:
        response = len(list)
        response_msg = u"Осталось изображений: " + str(response)
        bot.send_message(config.alarm_channel_name, text=response_msg)
    else:
        response = len(list)
    return response

def post_img_to_channel(channel_id, filename):
    img = open(filename, 'rb')
    bot.send_photo(channel_id, img)
    return 0

def move_file(file, sent_dir):
    new_name = get_timestamp()
    file_path, file_name = os.path.split(file)
    file_ext = file_name[file_name.rfind('.'):len(file_name):1]
    new_name = new_name+file_ext
    os.rename(file, file_path +'/'+ new_name)
    move(file_path +'/'+ new_name, sent_dir)
    return 0

def get_timestamp():
        now = datetime.datetime.now()
        year = str(now.year)
        month = str(now.month)
        day = str(now.day)
        hour = str (now.hour)
        minute = str(now.minute)
        if config.Debug == True:
            second = str(now.second)
            return year+month+day+hour+minute+second
        else:
            return year+month+day+hour+minute


if __name__ == "__main__":
    img_folder = config.img_dir
    img_list = get_img_list(img_folder)
    number_of_files = check_file_count(img_list)
    if number_of_files != 0:
        file_path = get_random_file(img_list, img_folder)
        post_img_to_channel(config.main_channel_name, file_path)
        post_img_to_channel(config.private_channel_name, file_path)
        if config.Debug == True:
            print(file_path)
        move_file(file_path, config.img_sent_dir)
    else:
        logging.error(u"There no images!")