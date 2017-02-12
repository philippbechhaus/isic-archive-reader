####### API ENPOINTS IMAGE #######

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


####### IMPORT PACKAGES #######
from urllib2 import urlopen
import json
import progressbar
import time, sys
import datetime
import multiprocessing


####### STATIC URL #######
def_url = 'https://isic-archive.com/api/v1/image'


####### GET.ID #######
def ids(limit):
    idsearch_url = def_url + '?limit=' + str(limit)
    idsearch_json = urllib2.urlopen(idsearch_url)
    idsearch_data = json.load(idsearch_json)
    ids = []
    for img in idsearch_data:
        ids.append(img['_id'])
    return ids


####### GET.URL #######
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


####### MULTIPROCESSING #######
def get_content(url):
    return json.load(urlopen(url))

def diagnosis_content(limit):
    a = datetime.datetime.now()
    URLS = urls(limit)
    pool = multiprocessing.Pool(processes=16)
    results = pool.map(get_content, URLS)
    pool.close()  # the process pool no longer accepts new tasks
    pool.join()   # join the processes: this blocks until all URLs are processed
    result_list = []
    for result in results:
        result_list.append(result['_id'] + ": " + result['meta']['clinical']['benign_malignant'])
    b = datetime.datetime.now()
    print(b-a)
    return result_list
