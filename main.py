import config
import telebot
import os
from shutil import move
from random import randrange
import datetime
import logging
import time
import re

bot = telebot.TeleBot(config.telegram_token)
logging.basicConfig(format = u'%(filename) s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level = logging.ERROR, filename=u'bot.log')


def try_send_message(channel_name, text):
    try:
        bot.send_message(channel_name, text=text)
    except telebot.apihelper.ApiException as e:
        logging.error(u"API Error:" + str(e))
        error_code = re.findall(r"\d\d\d", str(e.result))[0]
        if error_code == 500 or error_code == 502:
                logging.warning(u"Trying one more time request " + e.function_name)
                time.sleep(config.repeat_request_timeout)
                bot.send_message(channel_name, text=text)


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
        try_send_message(config.alarm_channel_name, text=response_msg)
    else:
        response = len(list)
    return response


def post_img_to_channel(channel_id, filename):
    img = open(filename, 'rb')
    try:
        bot.send_photo(channel_id, img)
    except telebot.apihelper.ApiException as e:
        logging.error(u"API Error:" + str(e))
        error_code = re.findall(r"\d\d\d", str(e.result))[0]
        if error_code == 500 or error_code == 502:
                error_msg = u"Trying one more time request " + e.function_name + ". Error:" + error_code
                logging.warning(error_msg)
                try_send_message(config.alarm_channel_name, error_msg)
                time.sleep(config.repeat_request_timeout)
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
    if Debug:
        return now.strftime("%Y%m%d%H%M%S")
    else:
        return now.strftime("%Y%m%d%H%M")


def main(folder):
    img_list = get_img_list(folder)
    number_of_files = check_file_count(img_list)
    if number_of_files != 0:
        file_path = get_random_file(img_list, folder)
        try_send_message(config.alarm_channel_name, text = file_path)
        post_img_to_channel(config.main_channel_name, file_path)
        post_img_to_channel(config.private_channel_name, file_path)
        #logging.error(filepath)
        if config.Debug == True:
            logging.info(file_path)
        move_file(file_path, config.img_sent_dir)
    else:
        logging.error(u"There no images!")


if __name__ == "__main__":
    main(config.img_dir)
