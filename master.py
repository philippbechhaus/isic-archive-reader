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
import urllib2
import json
import progressbar
import time, sys
import datetime


####### STATIC URL #######
def_url = 'https://isic-archive.com/api/v1/image'


####### IMAGE.ID SEARCH #######
def ids(limit):
    idsearch_url = def_url + '?limit=' + str(limit)
    idsearch_json = urllib2.urlopen(idsearch_url)
    idsearch_data = json.load(idsearch_json)
    ids = []
    for img in idsearch_data:
        ids.append(img['_id'])
    return ids

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

def diagnosis(limit):
    a = datetime.datetime.now()
    diag_list = urls(limit)
    result_list = []
    for temp in diag_list:
        temp_url = temp
        diagnosesearch_json = urllib2.urlopen(temp_url)
        diagnosesearch_data = json.load(diagnosesearch_json)
        result_list.append(diagnosesearch_data['_id'] + ": " + diagnosesearch_data['meta']['clinical']['benign_malignant'])
    b = datetime.datetime.now()
    print(b-a)
    return result_list
