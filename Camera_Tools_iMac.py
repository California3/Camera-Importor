# Developer: Guangming Zeng
# Copyright © 2023 G. Zeng / @堪培拉的一天seven
# Device: M1 Macbook Pro
# Name: Camera_Tools_XXX.py

# This script is used to:
# 1. Copy the files from the camera to the library.
# The files will be sorted by the days from the START_DATE.
# The files from the camera will be copied to the LIBRARY_PATH.
# 2. Move the files from the edited folder to the library.
# The JPG files will be moved to the EDITED_PATH.
# The optimized JPG files will be generated to the SLIM_PATH.

from PIL import Image, ExifTags, ImageDraw, ImageFont
import os
import time
import shutil
import concurrent.futures as cf
from alive_progress import alive_bar  # pip install alive_progress

sources = {
    "Zfc" : ['/Volumes/NIKON Z FC /DCIM'], # Nikon Zfc
    "Dji" : ['/Volumes/Untitled/DCIM','/Volumes/SD_Card/DCIM'], # DJI Action 2
}

skip_types           = ['LRF'] # Skip the files with these types.
JPG_support_types    = ['JPG'] # JPG files will be copied to the LIBRARY_PATH.
RAW_support_types    = ['NEF'] # RAW files will be copied to the LIBRARY_PATH.
Videos_support_types = ['MOV','MP4'] # Videos files will be copied to the LIBRARY_PATH.

LIBRARY_PATH = '/Users/u7100771/Library/CloudStorage/OneDrive-ArtGallery/Photos/Australia/Hundred 3' # The files will be copied to this path.
EDITED_PATH  = '/Users/u7100771/Pictures/Adobe Lightroom' # The files in this path will be moved to the LIBRARY_PATH.
SLIM_QUALITY = int(85) # The quality of the optimized JPG files.
START_DATE   = '2022-02-10' # This is Day 0. All the files will be sorted by the days from this date.

# TTF_Font = 'SourceSansPro-LightItalic.ttf'
# WATER_MARK = 'Copyright © 2023 G. Zeng / @堪培拉的一天seven'

files_queue = []
Day_Max = 0

def scan_file(search_path, tag):
    for file in scan_folder(search_path):
        if os.path.isdir(search_path + "/" + file):
            scan_file(search_path + "/" + file, tag)
        elif len(file.split(".")) > 1:
            this_file_name = file.split(".")[0]
            this_file_type = file.split(".")[1]
            file_location = search_path + "/" + file
            
            if this_file_type in skip_types:
                pass
            elif this_file_type in JPG_support_types:
                process_jpg(file_location, tag)
            elif this_file_type in RAW_support_types:
                process_raw(file_location, tag)
            elif this_file_type in Videos_support_types:
                process_video(file_location, tag)
            else:
                process_other(file_location, tag)

def process_jpg(file_location, tag):
    time_start = date_to_unix(START_DATE + ' 23:59:59')

    # print('-----------------')
    file = file_location.split("/")[-1]

    # get file creation date and time
    file_creation_date = os.path.getctime(file_location)
    # print in format of 2021-01-01
    create_date = time.strftime("%Y-%m-%d", time.localtime(file_creation_date)) + " 23:59:59"
    file_creation_date = date_to_unix(create_date)
    days = (file_creation_date - time_start) / 86400
    days = round(days)
    # print(file + " is " + str(days) + " days old")
    DAY = str(days)

    destination_path = LIBRARY_PATH + "/Day " + DAY + "/"+ tag + "_Preview"
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    destination_file = destination_path + "/" + file
    if not os.path.exists(destination_file):
        copy_action(file_location, destination_file)
        print(file_location + " will be copied.")
    else:
        print("File " + file + " already exists. Skip!")
        pass

def process_raw(file_location, tag):
    time_start = date_to_unix(START_DATE + ' 23:59:59')

    # print('-----------------')
    file = file_location.split("/")[-1]

    # get file creation date and time
    file_creation_date = os.path.getctime(file_location)
    # print in format of 2021-01-01
    create_date = time.strftime("%Y-%m-%d", time.localtime(file_creation_date)) + " 23:59:59"
    file_creation_date = date_to_unix(create_date)
    days = (file_creation_date - time_start) / 86400
    days = round(days)
    # print(file + " is " + str(days) + " days old")
    DAY = str(days)

    # Day_Max
    global Day_Max
    if int(DAY) > Day_Max:
        Day_Max = int(DAY)

    destination_path = LIBRARY_PATH + "/Day " + DAY + "/"+ tag + "_Raw"
    destination_path_Edited = LIBRARY_PATH + "/Day " + DAY + "/Edited"


    if not os.path.exists(destination_path_Edited):
        os.makedirs(destination_path_Edited)
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    destination_file = destination_path + "/" + file
    if not os.path.exists(destination_file):
        copy_action(file_location, destination_file)
        print(file_location + " will be copied.")
    else:
        print("File " + file + " already exists. Skip!")
        pass

def process_video(file_location, tag):
    time_start = date_to_unix(START_DATE + ' 23:59:59')

    # print('-----------------')
    file = file_location.split("/")[-1]

    # get file creation date and time
    file_creation_date = os.path.getctime(file_location)
    # print in format of 2021-01-01
    create_date = time.strftime("%Y-%m-%d", time.localtime(file_creation_date)) + " 23:59:59"
    file_creation_date = date_to_unix(create_date)
    days = (file_creation_date - time_start) / 86400
    days = round(days)
    # print(file + " is " + str(days) + " days old")
    DAY = str(days)

    destination_path = LIBRARY_PATH + "/Day " + DAY + "/"+ tag + "_Mov"
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    destination_file = destination_path + "/" + file
    if not os.path.exists(destination_file):
        copy_action(file_location, destination_file)
        print(file_location + " will be copied.")
    else:
        print("File " + file + " already exists. Skip!")
        pass

def process_other(file_location, tag):
    time_start = date_to_unix(START_DATE + ' 23:59:59')

    # print('-----------------')
    file = file_location.split("/")[-1]

    # get file creation date and time
    file_creation_date = os.path.getctime(file_location)
    # print in format of 2021-01-01
    create_date = time.strftime("%Y-%m-%d", time.localtime(file_creation_date)) + " 23:59:59"
    file_creation_date = date_to_unix(create_date)
    days = (file_creation_date - time_start) / 86400
    days = round(days)
    # print(file + " is " + str(days) + " days old")
    DAY = str(days)

    destination_path = LIBRARY_PATH + "/Day " + DAY + "/"+ tag + "_Other"
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    destination_file = destination_path + "/" + file
    if not os.path.exists(destination_file):
        copy_action(file_location, destination_file)
        print(file_location + " will be copied.")
    else:
        print("File " + file + " already exists. Skip!")
        pass

def scan_folder(search_path):
    print("Scanning " + search_path)
    scan = os.listdir(search_path)        
    # list reverse
    scan.reverse()
    return scan

def copy_action(file_location, destination_file):
    file_info = {
        'location': file_location, 
        'destination': destination_file
    }
    files_queue.append(file_info)
    # os.system('cp "' + file_location + '" "' + destination_file + '"')

def move_action(file_location, destination_file):
    copy_action(file_location, destination_file)

def commit_copy():
    if len(files_queue) == 0:
        return False
    print("Performing copy action concurrently...")
    with alive_bar(len(files_queue)) as bar: # 进度条
        with cf.ThreadPoolExecutor() as p: # 线程池
            for file_info in files_queue:
                file_location = file_info['location']
                destination_file = file_info['destination']
                p.submit(shutil.copy2, file_location, destination_file).add_done_callback(lambda func: bar())
    files_queue.clear()
    return True

def commit_move():
    if len(files_queue) == 0:
        return False
    print("Performing move action concurrently...")
    with alive_bar(len(files_queue)) as bar: # 进度条
        with cf.ThreadPoolExecutor() as p: # 线程池
            for file_info in files_queue:
                file_location = file_info['location']
                destination_file = file_info['destination']
                p.submit(shutil.move, file_location, destination_file).add_done_callback(lambda func: bar())
    files_queue.clear()
    return True

def commit_slim(slim_infos):
    print("Performing slim action concurrently...")
    with alive_bar(len(slim_infos)) as bar: # 进度条
        with cf.ThreadPoolExecutor() as p: # 线程池
            for slim_info in slim_infos:
                file_location = slim_info['save_location']
                destination_file = slim_info['slim_location']
                p.submit(slim_image, file_location, destination_file).add_done_callback(lambda func: bar())

def slim_image(file_location, destination_file):
    image = Image.open(file_location)
    image.save(destination_file, optimize=True, quality=SLIM_QUALITY, exif=image.info['exif'], progressive=True)

# change 2023-01-01 00:00:00 to unix timestamp
def date_to_unix(str):
    return int(time.mktime(time.strptime(str, "%Y-%m-%d %H:%M:%S")))
    
def process_edited_jpg(path, file):
    global Day_Max
    file_location = path + "/" + file
    time_start = date_to_unix(START_DATE + ' 23:59:59')
    print(file + " will be processed.")
    # get exif data
    exif = Image.open(file_location)._getexif()
    # get shot date and time
    shot_date = exif[36867]
    # print in format of 2021-01-01
    create_date = time.strftime("%Y-%m-%d", time.strptime(shot_date, "%Y:%m:%d %H:%M:%S")) + " 23:59:59"

    file_creation_date = date_to_unix(create_date)
    days = (file_creation_date - time_start) / 86400
    days = round(days)
    if days > Day_Max:
        Day_Max = days
    # print(file + " is " + str(days) + " days old")
    DAY = str(days)

    destination_path_Edited = LIBRARY_PATH + "/Day " + DAY + "/Edited"
    if not os.path.exists(destination_path_Edited):
        os.makedirs(destination_path_Edited)
    
    destination_path_Slim = LIBRARY_PATH + "/Day " + DAY + "/Slim"
    if not os.path.exists(destination_path_Slim):
        os.makedirs(destination_path_Slim)

    # print(DAY)
    file_info = {
        'location': file_location, 
        'slim_location': destination_path_Slim + "/" + file,
        'save_location': destination_path_Edited + "/" + file
    }
    # image_width, image_height = image.size
    # draw = ImageDraw.Draw(image)
    # font = ImageFont.truetype(TTF_Font, 70)
    # txt_width, txt_height = draw.textsize(WATER_MARK, font=font)
    # draw.text((image_width - txt_width - 50, image_height - txt_height - 50), WATER_MARK, font=font, fill=(255, 255, 255, 128))

    #image.save(file_info['slim_location'], optimize=True, quality=SLIM_QUALITY, exif=image.info['exif'], progressive=True)
    move_action(file_info['location'], file_info['save_location'])
    return file_info

# main function
if __name__ == '__main__':
    # check if destination folder exists
    if not os.path.exists(LIBRARY_PATH):
        raise Exception("Destination folder not found")

    is_Copy = False
    for tag, source_list in sources.items():
        # check source_list is a list and not empty
        if not isinstance(source_list, list) or len(source_list) == 0:
            continue
        for source in source_list:
            if source == '':
                continue
            if os.path.exists(source):
                scan_file(source, tag)
                status = commit_copy()
                is_Copy = status or is_Copy

    if is_Copy:
        print("Found New Camera Files.")
        if Day_Max > 0:
            DAY = str(Day_Max)
            destination_path = LIBRARY_PATH + "/Day " + DAY + ""
            # open folder
            os.system('open "' + destination_path + '"')
        else:
            destination_path = LIBRARY_PATH
            # open folder
            os.system('open "' + destination_path + '"')
    else:
        print("No New Camera Files.")
        His_Day = Day_Max
        # check if export folder exists
        if not os.path.exists(EDITED_PATH):
            raise Exception("Export folder not found")
        Day_Max = 0
        # export_path
        slim_infos = []
        for file in scan_folder(EDITED_PATH):
            if file.endswith(".jpg"):
                info = process_edited_jpg(EDITED_PATH, file)
                slim_infos.append(info)
        if commit_move():
            commit_slim(slim_infos)
            slim_infos.clear()
            if Day_Max > 0:
                DAY = str(Day_Max)
                destination_path = LIBRARY_PATH + "/Day " + DAY + "/Slim"
                # open folder
                os.system('open "' + destination_path + '"')
            else:
                destination_path = LIBRARY_PATH
                # open folder
                os.system('open "' + destination_path + '"')
        else:
            print("No New Edited Files.")
            DAY = str(His_Day)
            destination_path = LIBRARY_PATH + "/Day " + DAY + ""
            # open folder
            os.system('open "' + destination_path + '"')