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
from flask import Flask, jsonify, request

import asyncio
from douyin_tiktok_scraper.scraper import Scraper

api = Scraper()
app = Flask(__name__)

class TikTok_Crawl:
    def __init__(self, link_crawl_video: str):
        self.valid_url = False
        self.link_crawl_video = link_crawl_video
        self.check_url()
        if self.valid_url:
            try:
                # ua = UserAgent()
                # header = {'User-Agent':str(ua.chrome)}
                # link_video = link_crawl_video
                # response = requests.get(link_video, cookies=cookies, timeout=(10, 10))
                # # print(f'{link_video}:{response.text}')
                # print(type(response.text))
                # options = Options()
                # options.add_argument("start-maximized")
                # # options.add_argument("--headless")
                # # options.add_argument('headless')
                # options.add_argument("--disable-blink-features=AutomationControlled")
                # options.add_experimental_option("excludeSwitches", ["enable-automation"])
                # driver = webdriver.Chrome(options=options)
                # driver.get(link_video)
                # driver.implicitly_wait(10)
                # last_url = driver.current_url;
                # self.link_download_video = last_url;
                # print(driver.page_source)
                # driver.quit()
                return
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

    async def get_tiktok_video_data(self, video_id):
        video_data = await api.get_tiktok_video_data(video_id)
        video = video_data['video']
        title = video_data['author']['nickname']
        desc = video_data['desc']
        cover = video['cover']['url_list'][0]
        download_link = video['play_addr']['url_list'][0]
        print(f"title: {title}, desc: {desc}, cover: {cover}, download_link: {download_link}")
        # print(video_data['video'])
    
async def main():
    link = 'https://www.tiktok.com/@slopbogbinky/video/7159283308063477035'
    crawl_vid_TikTok = TikTok_Crawl(link)
    await crawl_vid_TikTok.get_tiktok_video_data('7290942038466465067')    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())