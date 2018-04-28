import requests
from threading import Thread
import xml.etree.ElementTree
import unicodedata

Devices = [
    {'0' : "Temperature"},
    {'1' : "Humidity"},
    {'2' : "Motion"},
    {'3' : "Alien Presence"},
    {'4' : "Dark Matter"},
    {'5' : "Top Secret"}]

URL = "https://desolate-ravine-43301.herokuapp.com/"
DeviceList = []

URLList = []
Secret_key_header = {}

threads = []

url_count = 0
processed_urls = 0

def get_private_key():

    global url_count
    
    r = requests.post(URL)

    json = r.json()

    headers = r.headers
    secret_key = headers['Session']
    Secret_key_header = {"Session" : secret_key}

    # print(Secret_key_header)

    for urlItem in json:
        
        URLList.append(urlItem)

    url_count = len(URLList)

    return Secret_key_header
    
    print(URLList)
    # print(r.json())

def get_data(url):

    global processed_urls, url_count, DeviceList

    if(url['method'] == 'GET'):
        r = requests.get(URL + url['path'], headers=Secret_key_header)
    else:
        r = requests.post(URL + url['path'], headers=Secret_key_header)

    response_format = r.headers['Content-Type']

    # print(Secret_key_header)d
    # print(r.text)

    if(response_format == "Application/json"):
        
        json_response = r.json()

        tempObj = {}
        tempObj = {"id": json_response["device_id"], "type": json_response["sensor_type"], "value": json_response["value"]}

        DeviceList.append(tempObj)

    elif(response_format == "Application/xml"):

        e = xml.etree.ElementTree.fromstring(r.text)

        tempObj = {"id" : e.attrib['id']}

        for child in e:
            if(child.tag == "type"):
                tempObj['type'] = child.text
            else:
                tempObj['value'] = child.text

        DeviceList.append(tempObj)


    else:
        response_text = r.text
        splitted_text = response_text.split("\n")

        for i in range(len(splitted_text)):
            if i != 0:
                split_new_text = splitted_text[i].split(",")

                if len(split_new_text) == 3:

                    device_id = unicodedata.normalize('NFKD', split_new_text[0]).encode('ascii', 'ignore')

                    tempObj = {"id": device_id, "type": int(split_new_text[1]), "value": float(split_new_text[2])}

                    DeviceList.append(tempObj)

        # print(splitted_text)
    
    processed_urls += 1

    if(processed_urls == url_count):
        show_final_result()
    

def show_final_result():
    for i in range(len(Devices)):
        if(i == 0):
            print
            deviceType = Devices[i]
            deviceName = deviceType['0']
            print(deviceName)
            for device in DeviceList:
                if(device['type'] == i):
                    print('Device ' + device['id'] + ' - ' + str(device['value']))
        elif(i == 1):
            print
            deviceType = Devices[i]
            deviceName = deviceType['1']
            print(deviceName)
            for device in DeviceList:
                if(device['type'] == i):
                    print('Device ' + device['id'] + ' - ' + str(device['value']))
        elif(i == 2):
            print
            deviceType = Devices[i]
            deviceName = deviceType['2']
            print(deviceName)
            for device in DeviceList:
                if(device['type'] == i):
                    print('Device ' + device['id'] + ' - ' + str(device['value']))
        elif(i == 3):
            print
            deviceType = Devices[i]
            deviceName = deviceType['3']
            print(deviceName)
            for device in DeviceList:
                if(device['type'] == i):
                    print('Device ' + device['id'] + ' - ' + str(device['value']))
        elif(i == 4):
            print
            deviceType = Devices[i]
            deviceName = deviceType['4']
            print(deviceName)
            for device in DeviceList:
                if(device['type'] == i):
                    print('Device ' + device['id'] + ' - ' + str(device['value']))
        else:
            print
            deviceType = Devices[i]
            deviceName = deviceType['5']
            print(deviceName)
            for device in DeviceList:
                if(device['type'] == i):
                    print('Device ' + device['id'] + ' - ' + str(device['value']))
        print



def get_parallel_requests():
    for url in URLList:
        threads = []
        threads.append(Thread(target=get_data, args=(url,)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

Secret_key_header = get_private_key()
get_parallel_requests()