import json
import urllib3
import sys
import math
import time
import random
import logging
import socket
import importlib

stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
importlib.reload(sys)
sys.getdefaultencoding()
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde

fmt = '%(asctime)s %(filename)s[line: %(lineno)d] %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG,
                    format=fmt,
                    filename='logs.txt',
                    filemode='a',
                    datefmt='%a, %d %b %Y %H:%M:%S'
                    )

def request_ajax_data(url, referer=None, **headers):
    req = urllib3.Request(url)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('X-Requested-With', 'XMLHttpRequest')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116')
    req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
    req.add_header('Client-ID', 'mr9jlh9wbcptpo1dd04kwo88v79oi5')
    if referer:
        req.add_header('Referer', referer)
    if headers:
        for k in headers.keys():
            req.add_header(k, headers[k])

    NET_STATUS = False
    while not NET_STATUS:
        try:
            response = urllib3.urlopen(req, data=None, timeout=3) # response = urllib2.urlopen(req)
            jsonText = response.read()
            logging.info('NET_STATUS is good')
            return json.loads(jsonText)           
        except socket.timeout:
            logging.info('NET_STATUS is not good')
            NET_STATUS = False

def save_list(tmp_list, file_name): 
    with open(file_name, 'a') as outfile:
        json.dump(tmp_list, outfile, ensure_ascii=False)
        outfile.write('\n')
        
def print_time(file_name):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) 
    with open(file_name, 'a') as outfile:
        json.dump(current_time, outfile, ensure_ascii=False)
        outfile.write('\n')

def request_data(game_id):
    file_name = ('./' + str(game_id) + '_streams_'+current_date+'.json')
    print_time(file_name)
    
    tmp_list = []
    count = 0
    
    url = 'https://api.twitch.tv/helix/streams?game_id=' + str(game_id) + '&first='+str(num_each_time)
   
    while True:
        try:
            streams = request_ajax_data(url)
            break
        except:
            logging.info('except...')
            time.sleep(5)
            continue

    streams_data = streams['data']       
    streams_cursor = streams['pagination']['cursor']

    tmp_list.extend(streams_data)
    count = count + len(streams_data)
    logging.info(str(game_id) + ' ' + str(count))  

    if len(streams_data) < num_each_time:
        save_list(tmp_list, file_name)
        
    while len(streams_data) == num_each_time:
        url = ('https://api.twitch.tv/helix/streams?game_id=' + str(game_id) + '&first='+str(num_each_time)+'&after='+streams_cursor)
        try:
            time.sleep(random.randint(0, 1))
            streams = request_ajax_data(url)
        except:
            logging.info('except..')
            time.sleep(5)
            continue
            
        streams_data = streams['data']
        tmp_list.extend(streams_data)
        count = count + len(streams_data)
        logging.info(str(game_id) + ' ' + str(count))

        if count % 1000 == 0:
            save_list(tmp_list, file_name)
            tmp_list = []

        if streams['pagination']:
            streams_cursor = streams['pagination']['cursor']
            logging.info(streams_cursor)
        else:
            save_list(tmp_list, file_name)
            break

        if len(streams_data) < num_each_time:
            save_list(tmp_list, file_name)
            break

if __name__ == "__main__":
    Game_ID = []  # Initialize Game_ID before using it
    
    load_file_name = '/Users/duboisrenan/Les-Petit-chou/GameTitle.txt'
    with open(load_file_name) as f:
        line = f.readline()

        while line:
            line_split = line.split('\t')
            if len(line_split) > 1:
                Game_ID.append(line_split[1][0:len(line_split[1])-1])
            line = f.readline()
    
    num_each_time = 100
    collect_time = 15
    
    while True:
        current_date = time.strftime('%y%m%d', time.localtime(time.time()))
 
        current_tmp = time.strftime('%M-%S', time.localtime(time.time()))
        current_time = int(current_tmp.split('-')[0]) * 60 + int(current_tmp.split('-')[1])
        wait_time = collect_time - int(current_time) % collect_time
        time.sleep(wait_time)
 
        for index in range(len(Game_ID)):
            request_data(Game_ID[index])
