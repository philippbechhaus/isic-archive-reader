'''
+--------------------+
| API ENPOINTS IMAGE |
+--------------------+

# GET /image Return a list of lesion images.

# Parameter	Data Type  Description
# limit     integer    Result set size limit
# offset	integer    Offset into result set
# sort      string     Field to sort the result set by
# sortdir   integer	   Sort order: 1 for ascending, -1 for descending
# datasetId	string     The ID of the dataset to use
# name	    string     Find an image with a specific name
# filter	string     Filter the images by a PegJS-specified grammar (causing "datasetId" and "name" to be ignored)

# GET /image/{id} Return an image's details.
# GET /image/{id}/download Download an image's high-quality original binary data.
# POST /image/{id}/segment Run and return a new semi-automated segmentation.
# GET /image/{id}/superpixels Get the superpixels for this image, as a PNG-encoded label map.
# GET /image/{id}/thumbnail Return an image's thumbnail.
# GET /image/histogram Return histograms of image metadata.
'''

'''
+-------------------------------------------------------------------------------------------------------------+
| To optimize downloading speed, each function contains a timer that prints out lapsed time for given process |
+-------------------------------------------------------------------------------------------------------------+
'''

# Import packages
from urllib.request import urlopen
from urllib.request import urlretrieve
import json
import time, sys
import datetime
import multiprocessing
import os
from PIL import Image
import uuid
import shutil

# Import API
def_url = 'https://isic-archive.com/api/v1/image'


# Get ID
def ids(limit):
    idsearch_url = def_url + '?limit=' + str(limit)
    idsearch_json = urlopen(idsearch_url)
    idsearch_data = json.load(idsearch_json)
    ids = []
    for img in idsearch_data:
        ids.append(img['_id'])
    return ids


# Get URL
def urls(limit):
    a = datetime.datetime.now()
    temp_list = ids(limit)
    new_list = []
    nr = 0
    for i in temp_list:
        temp = def_url + '/' + temp_list[nr]
        new_list.append(temp)
        nr += 1
    b = datetime.datetime.now()
    print(b-a)
    return new_list

# Get Download Link
def d_urls(limit):
    a = datetime.datetime.now()
    temp_list = ids(limit)
    new_list = []
    nr = 0
    for i in temp_list:
        temp = def_url + '/' + temp_list[nr] + '/download'
        new_list.append(temp)
        nr += 1
    b = datetime.datetime.now()
    print(b-a)
    return new_list


# Get diagnosis for each image ID
# Concatenate tuple and store in list
# Run method with multiple processes
def get_content(url):
    return json.load(urlopen(url))

def diagnosis(limit):
    # Set process limit:
    process_limit = 16
    # Method start:
    a = datetime.datetime.now()
    URLS = urls(limit)
    pool = multiprocessing.Pool(processes=process_limit)
    results = pool.map(get_content, URLS)
    pool.close()  # the process pool no longer accepts new tasks
    pool.join()   # join the processes: this blocks until all URLs are processed
    result_list = []
    for result in results:
        result_list.append(result['_id'] + "." + result['meta']['clinical']['benign_malignant'])
    b = datetime.datetime.now()
    print(b-a)
    return result_list

# Creates list with RGB code of each images
# Creates temp folder to store downloaded images
# After conversion, deletes folder
# Run with multiple processes
rgblist = []
dir_path = os.path.dirname(os.path.realpath(__file__))

def get_id(url):
    temp = url.split('/')
    return temp[6]

def get_image_help(url):
    return urlretrieve(url,os.path.join(dir_path+"/images",str(
    get_id(url))+'.jpg'))

def convert_to_rgb(limit):
    a = datetime.datetime.now()
    images = get_image(limit)
    for image in images:
        img = Image.open(image[0])
        imglist = list(img.getdata())
        rgblist.append(imglist)
    b = datetime.datetime.now()
    print (b-a)
    return

# Main
if __name__ == '__main__':
    print("ISIC Archive Reader" "\n" "Code by Philipp Bechhaus" "\n" "\n")
    while True:
        try:
            limit = int(input("How many images would you like to extract?" "\n" "\n"))
        except NameError:
            print("That's not a number!")
        except SyntaxError:
            print("That's not a number!")
        else:
            if limit > 0:
                break
            else:
                print("Please select at least 1" "\n" "\n")

    while True:
        try:
            selection = int(input("Which method would you like to run? " "\n" "\n" "Select" "\n" "1 for a list of download URLs"
                           "\n" "2 for a list of diagnoses with corresponding Image UUID" "\n" "3 for a list of RGB converted images with corresponding UUID" "\n" "\n"))
        except NameError:
            print("That's not a number!")
        except SyntaxError:
            print("That's not a number!")
        else:
            if selection > 0 and selection <= 3:
                break
            else:
                print("Please select either 1, 2 or 3" "\n" "\n")

    if selection == 1:
        temp = d_urls(limit)
        for te in temp:
            print(te)
    elif selection == 2:
        temp = diagnosis(limit)
        for te in temp:
            print(te)
    elif selection == 3:
        convert_to_rgb(limit)
        for te in rgblist:
            print(te)
