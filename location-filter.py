import json
import requests
import numpy as np
import matplotlib.path as mplPath

# Creating Yemen Bounding Box
# Latitude is up down - Longitude is left right
topLeft = [17.18, 41.81]
topRight = [19.52, 51.85]
bottomLeft = [12.25, 43.39]
bottomRight = [15.45, 53.99]
bbPath = mplPath.Path(np.array([topLeft, topRight, bottomRight, bottomLeft]))

# JSON location
jsonFile = 'tweet_locations_stripped.json'


def main():
    with open(jsonFile) as data_file:
        data = json.load(data_file)

    filtered_data = data

    for username in data:
        for text in filtered_data[username]:
            delete = True
            # Prints actual tweet
            # print text['text']

            decoded = entityExtract(text['text']).json()

            for i, entry in enumerate(decoded):
                if entry['tag'] == "LOCATION":
                    lCheck = coordinateLocation(entry['label']).json()
                    for j, coord in enumerate(lCheck):
                        lat = coord['latitude']
                        lon = coord['longitude']

                        if bbPath.contains_point((lat, lon)):
                            # print entry['label'] + " has coordinates (" + str(lat) + ", " + str(lon) + ")."
                            delete = False
                            break;
            if delete is True:
                del text['text']
                del text['time']

    dumpclean(filtered_data)

def entityExtract(text):
    headers = {'Content-Type' : 'application/json'}
    body = json.dumps({ "text": text, "extract_type": "mitie"})
    r = requests.post('http://54.174.131.124:3003/api/extract/run', data=body, headers=headers)
    # print (r.content)
    return r

def coordinateLocation(location):
    headers = {'Content-Type' : 'application/json'}
    body = json.dumps({ "address": location, "extract_type": "mitie"})
    r = requests.post('http://54.174.131.124:3003/api/geocoder/forward-geo', data=body, headers=headers)
    return r

def buildJson():
    return

def dumpclean(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print k
                dumpclean(v)
            else:
                print '%s : %s' % (k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print v
    else:
        print obj

main()