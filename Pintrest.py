import requests
import re
import json

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