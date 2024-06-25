import requests
import re
import json
from bs4 import BeautifulSoup
import time

class Pintrest:
    def __init__(self,url) -> None:
        self.url = url
    def is_url_valid(self):
        if re.match(r'(^http(s)?://)?(www.)?pinterest.\w+/pin/[\w\-?]+',self.url) or re.match(r'^https://pin\.it/[a-zA-Z0-9]+',self.url) :
            return True
        return False
    def get_page_content(self):
        content = requests.get(self.url).text
        return content
    def is_a_video(self):
        if "video-snippet" in self.get_page_content():
            return True
        return False
    def get_media_Link(self):
        if self.is_url_valid():
            try:
                if self.is_a_video():
                    match = re.findall(r'<script data-test-id="video-snippet".+?</script>',self.get_page_content())
                    j = json.loads(match[0].replace('<script data-test-id="video-snippet" type="application/ld+json">',"").replace("</script>",""))
                    return {"type":"video","link":j["contentUrl"],"success":True}
                else:
                    match = re.findall(r'<script data-test-id="leaf-snippet".+?</script>',self.get_page_content())
                    j = json.loads(match[0].replace('<script data-test-id="leaf-snippet" type="application/ld+json">',"").replace("</script>",""))
                    j["image"]
                    return {"type":"image","link":j["image"],"success":True}
            except:
                return {"type":"2","link":"","success":False}
        else:
            return {"type":"1","link":"","success":False}
        
    def get_pinterest_video(self, page_url):
        t_body = requests.get(page_url)
        if(t_body.status_code != 200):
            print("Entered URL is invalid or not working.")
        soup = BeautifulSoup(t_body.content,"html.parser")
        href_link = (soup.find("link",rel="alternate"))['href']
        match = re.search('url=(.*?)&', href_link)
        page_url = match.group(1) # update page url 

        print("fetching content from given url")
        body = requests.get(page_url) # GET response from url
        if(body.status_code != 200): # checks status code
            print("Entered URL is invalid or not working.")
        else:
            soup = BeautifulSoup(body.content, "html.parser") # parsing the content
            print("Fetched content Sucessfull.")
            ''' extracting the url
            <video
                autoplay="" class="hwa kVc MIw L4E"
                src="https://v1.pinimg.com/videos/mc/hls/......m3u8"
                ....
            ></video>
            '''
            extract_url = (soup.find("video",class_="hwa kVc MIw L4E"))['src'] 
            # converting m3u8 to V_720P's url
            convert_url = extract_url.replace("hls","720p").replace("m3u8","mp4")
            return convert_url

    def get_pinterest_image(self, pinterest_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(pinterest_url, headers=headers)
            response.raise_for_status()  # Kiểm tra mã trạng thái HTTP

            soup = BeautifulSoup(response.content, 'html.parser')
            media_tag = soup.find('meta', property='og:video') or soup.find('meta', property='og:image')
            
            if media_tag:
                return media_tag['content']
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        
    def get_media_LinkV2(self):
        if self.is_url_valid():
            try:
                if self.is_a_video():
                    media_url = self.get_pinterest_video(self.url)
                    return {"type":"video","link":media_url,"success":True}
                else:
                    media_url = self.get_pinterest_image(self.url)
                    return {"type":"image","link":media_url,"success":True}
            except Exception as err:
                print('Error get_media_LinkV2: ', err)
                return {"type":"2","link":"","success":False}
        else:
            return {"type":"1","link":"","success":False}
        
    