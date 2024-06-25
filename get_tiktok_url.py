import time
import requests
import traceback
import json
import os
import os.path as osp
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from config import params, cookies, headers
from fake_useragent import UserAgent
import json
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify, request, send_from_directory
from Pintrest import Pintrest

from douyin_tiktok_scraper.scraper import Scraper

import re
from urllib.parse import urlparse, parse_qs
from common_function import is_instagram_link

api = Scraper()

app = Flask(__name__)

listAllowedIP = ['']
SECCRET_KEY = 'tCtEZDbkdfLqA5g11wIh7oUfgZREZhvC'

class TikTok_Crawl:
    def __init__(self, link_crawl_video: str):
        self.valid_url = False
        self.link_crawl_video = link_crawl_video
        self.check_url()
        if self.valid_url:
            try:
                ua = UserAgent()
                header = {'User-Agent':str(ua.chrome)}
                link_video = link_crawl_video
                data = {
                    'videoUrl': link_video,
                }
                response = requests.post('https://www.watermarkremover.io/api/video', cookies=cookies, headers=header, data=data, timeout=(10, 10))
                print(f'{link_video}:{response.text}')
                print(type(response.text))
                responseJson = json.loads(response.text)
                downloadLink = responseJson["nowm"]
                print(downloadLink)
                options = Options()
                options.add_argument("start-maximized")
                # options.add_argument("--headless")
                options.add_argument('headless')
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                driver = webdriver.Chrome(options=options)
                driver.get(downloadLink)
                driver.implicitly_wait(10)
                last_url = driver.current_url;
                self.link_download_video = last_url;
                # print(last_url)
                # # request=urllib.request.Request(downloadLink)
                # # page = urlopen(request).read()
                # # print(page)
                # mp4File = urlopen(last_url)
                # # Feel free to change the download directory
                # f_video = osp.join(os.getcwd(), 'temp', f'123.mp4')
                # with open(f_video, "wb") as output:
                #     while True:
                #         data = mp4File.read(4096)
                #         if data:
                #             output.write(data)
                #         else:
                #             break
            except Exception as e:
            # By this way we can know about the type of error occurring
                print("The error is: ",e)
    
    
    # check url is valid or not valid
    def check_url(self):
        req = requests.get(self.link_crawl_video)
        if req.status_code == 200:
            self.valid_url = True

@app.route('/tmp/<path:image_name>')
def get_tmp_image(image_name):
    # Replace '/tmp' with the actual directory path
    return send_from_directory('tmp', image_name)

@app.route('/get_tiktok_url', methods=['POST'])
def get_tiktok_url():
    dataBody = request.form
    video_url = dataBody['video_url'] 
    crawl_vid_TikTok = TikTok_Crawl(video_url)
    print(crawl_vid_TikTok.link_download_video)
    # print(request.data)
    # print(request.form)
    return jsonify({ 'status': 200, 'url_download': crawl_vid_TikTok.link_download_video })
    # dataBody = json.loads(request.data)    

@app.route('/get_tiktok_video_data', methods=['GET'])
async def get_tiktok_video_data():
    time.sleep(1)
    video_id = request.args.get('video_id') 
    video_data = await api.get_tiktok_video_data(video_id)
    video = video_data['video']
    title = video_data['author']['nickname']
    desc = video_data['desc']
    cover = video['cover']['url_list'][0]
    download_link = video['play_addr']['url_list'][0]
    print(f"title: {title}, desc: {desc}, cover: {cover}, download_link: {download_link}")
    return jsonify({ 
        'title': title, 
        'desc': desc, 
        'cover': cover, 
        'download_link': download_link, 
        })

@app.route('/get_pinterest_url', methods=['POST'])
def get_pinterest_url():
    dataBody = request.form
    pin_url = dataBody['pin_url'] 
    pin = Pintrest(pin_url)
    response = pin.get_media_LinkV2()
    if response['success'] == True:
        return jsonify({ 'status': 200, 'url_download': response['link'], 'type': response['type'] }) 
    return jsonify({ 'status': 400, 'message': 'Not working' })    

@app.route('/get_insta_url', methods=['POST'])
def get_insta_url():
    # Get client's IP address
    client_ip = request.remote_addr
    print("Client IP:", client_ip)
    # Check if the client's IP address is allowed
    if (client_ip in listAllowedIP or request.headers.get('X-SECRET-KEY') == SECCRET_KEY) == False:
        return jsonify({ 'status': 400, 'message': 'Not allowed' })

    dataBody = request.form
    insta_url = dataBody['insta_url'] 
    try:
        start_time = time.time()
        code_match = re.search(r'/(p|reels|reel)/([^/]+)/', insta_url)
        # validate link_video is instagram link
        isValidLink = is_instagram_link(insta_url)
        print(isValidLink)
        if not isValidLink:
            # print("Invalid Instagram link.")
            return jsonify({ 'status': 400, 'message': 'Invalid URL' }) 

        if code_match:
            code = code_match.group(2)
            print("Code:", code)
        else:
            print("Code not found in URL.")
            return jsonify({ 'status': 400, 'message': 'Code not found in URL' }) 
        time.sleep(1)
        data = {
            't': 'media',
            'lang': 'vi',
            'q': insta_url
        }
        ua = UserAgent()
        print(ua.chrome)
        headers_random = {'user-agent': str(ua.chrome)}
        # print(header)
        # Request post
        response = requests.post('https://snapinsta.io/api/ajaxSearch', params=params, cookies=cookies, data=data, timeout=(10, 10))
        jsonResponse = json.loads(response.text);
        # print(type(response.text))
        downloadSoup = BeautifulSoup(jsonResponse["data"], "html.parser")
        # exit()
        # print(downloadSoup)
        listItemsDownload = downloadSoup.find_all('div', class_='download-items')
        listLinkDownload = []
        listLinkPreview = []
        for child in listItemsDownload:

            if child.findChildren(recursive=False):
                # print(child.img['src'])
                linkDownload = child.a['href']
                listLinkDownload.append(linkDownload)
                # print(linkDownload)
        # print(listItemsDownload)
        # downloadLink = downloadSoup.a["href"]
        # print(downloadLink)
        # check tmp folder exist if not create
        if not osp.exists('tmp'):
            os.makedirs('tmp')
        # create folder with code name with template: tmp/{code}
        folderName = 'tmp/' + code + '/'
        if not osp.exists(folderName):
            os.makedirs(folderName)
    
        # download all media of link in listLinkDownload to tmp folder
        for link in listLinkDownload:
            # print(link)
            # Parse the URL
            parsed_url = urlparse(link)

            # Extract the file name from the path
            file_name = parsed_url.path.split('/')[-1]
            full_path = folderName + file_name
            # check if file exist in folder
            if osp.exists(full_path):
                print("File exist")
                listLinkPreview.append(full_path)
                continue
            response = requests.get(link, headers=headers_random)
            mime_type = response.headers.get('Content-Type')
            print(mime_type)
            if mime_type == 'video/mp4':
                full_path = full_path + '.mp4'
                # file_name = file_name + '.mp4'
            # print(mime_type)
            # continue
            with open(full_path, 'wb') as file:
                file.write(response.content)
                listLinkPreview.append(full_path)
        print("--- %s seconds ---" % (time.time() - start_time))
        return jsonify({ 'status': 200, 'code': code, 'url_download': listLinkDownload, 'url_preview': listLinkPreview, 'type': '' }) 
        # exit()
        # videoTitle = downloadSoup.p.getText().strip()
        # results[data['id']] = {
        #     'link_watermark': data['id'],
        #     'link_without_watermark': downloadLink,
        #     'videoTitle': videoTitle,
        #     'time_crawl': time.time()
        # }
        # print(results)
    except Exception as err:
        print('Error: ', err)
        return jsonify({ 'status': 400, 'message': 'Not working' })  
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug = False)