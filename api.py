import json
import math
import requests
import time

'''adr = raw_input('Address ')'%d.%m.%Y %H:%M:%S'
date_time = str(raw_input('Start time '))
pattern = '%Y-%m-%d %H:%M:%S'
bgn_input = int(time.mktime(time.strptime(date_time, pattern)))*1000 - 1800000
end_input = bgn_input + 7200000'''


def make_response(lat, long, results_count=1):
    params = {
        'geocode': '%s,%s' % (lat, long),
        'kind': 'locality',
        'format': 'json',

        'results': results_count
    }
    r = requests.get('https://geocode-maps.yandex.ru/1.x/', params=params)
    return r.json()


def make_response2(adr, results_count=1):
    params = {
        'geocode': '%s' % (adr),
        'format': 'json',
        'results': results_count
    }
    r2 = requests.get('https://geocode-maps.yandex.ru/1.x/', params=params)
    return r2.json()


def process_response(resp):
    t1 = resp["response"]["GeoObjectCollection"]["featureMember"]
    if len(t1) == 0:
        return None
    t1 = t1[0]
    t1 = t1["GeoObject"]['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']
    if t1['AdministrativeArea'].keys()[0] == 'SubAdministrativeArea':
        return t1['AdministrativeArea']['SubAdministrativeArea']['Locality']['LocalityName']
    else:
        return t1['AdministrativeArea']['Locality']['LocalityName']


def do_your_worst(lat, long):
    return u"%s" % process_response(make_response(lat, long))


def get_locales(limit=1000, offset=0):
    params = {
        'limit': limit,
        'offset': offset,
        'fields': 'name'
    }
    r = requests.get("https://all.culture.ru/api/2.2/locales", params=params)
    return r.json()


def read_locales(fname='culture_locales.json'):
    """ Reads locales from json and returns list of locales objects """
    locales = None
    with open(fname) as fp:
        locales = json.load(fp)
    return locales

def get_coordinates(adr):
    almost_coordinates = make_response2(adr, results_count=1)
    coordinates = almost_coordinates['response']['GeoObjectCollection']['featureMember']
    almost_lat = coordinates[0]['GeoObject']['Point']['pos'][10:19]
    almost_longt = coordinates[0]['GeoObject']['Point']['pos'][:9]
    lat_input = float(almost_longt)
    longt_input = float(almost_lat)
    return lat_input, longt_input

#lat_input = 56.804024
#longt_input = 37.274763
'''
area = do_your_worst(lat_input, longt_input).lower()

for pair in read_locales():
    if pair['name'].lower() == area:
        id_area = pair['_id']
'''

def make_response3(locales_id, start, end, off=0, limit=100):
    events = []
    params = {
        'locales': '%s' % (locales_id),
        'start': '%s' % (start),
        'end': '%s' % (end),
        'offset': '%s' % (off),
        'limit': '%s' % (limit),
        'format': 'json',
    }

    params['limit'] = 1
    r = requests.get('https://all.culture.ru/api/2.2/events?', params=params)
    total = r.json()['total']

    params['limit'] = limit
    off = 0
    while off < total:
        params['offset'] = off
        r = requests.get('https://all.culture.ru/api/2.2/events?', params=params)
        off += limit
        events += r.json()['events']
    return events

def get_list(id_area, bgn_input, end_input):
    obj = make_response3(id_area, bgn_input, end_input)
    ev_dist = {}
    for event in obj:
        if event['status'] == 'accepted':
            nmbr_pl = 0
            while nmbr_pl < len(event['places']):
                name = event.get('altName')
                #begins = event['start']
                #ends = event['end']

                # if ends > bgn_input and begins < end_input:
                for seance in event['seances']:
                    if bgn_input > seance['start'] and bgn_input < seance['end']:
                        latitude = event['places'][nmbr_pl]['address']['mapPosition']['coordinates'][0]
                        longitude = event['places'][nmbr_pl]['address']['mapPosition']['coordinates'][1]
                        rad = 6372795
                        lat1 = latitude * math.pi / 180.
                        lat2 = longt_input * math.pi / 180.
                        longt1 = longitude * math.pi / 180.
                        longt2 = lat_input * math.pi / 180.
                        cl1 = math.cos(lat1)
                        cl2 = math.cos(lat2)
                        sl1 = math.sin(lat1)
                        sl2 = math.sin(lat2)
                        delta = longt2 - longt1
                        cdelta = math.cos(delta)
                        sdelta = math.sin(delta)
                        y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
                        x = sl1 * sl2 + cl1 * cl2 * cdelta
                        ad = math.atan2(y, x)
                        dist = ad * rad
                        ev_dist[name] = dist
                nmbr_pl += 1

    sorted_ev_dist = sorted(ev_dist.items(), key=lambda (k, v): v, reverse=False)
    ten_sorted_ev_dist = sorted_ev_dist[:10]

    output = ''
    for each in ten_sorted_ev_dist:
        for event in obj:
            if event.get('altName') == each[0]:
                output += each[0]+'\n'+event['shortDescription']+event['externalInfo'][0]['url']+'\nPrice: '+str(event['price'])+'\nDistance: '+str(int(round(each[1])))+'m'+'\n'
    return output
