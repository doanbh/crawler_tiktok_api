import re

def is_instagram_link(link):
    # Regular expression pattern for Instagram video links
    pattern = r'^https?:\/\/(?:www\.)?instagram\.com\/(?:p|reel)\/[a-zA-Z0-9_-]+\/?(?:\?.*)?$'
    
    # Check if the link matches the pattern
    if re.match(pattern, link):
        return True
    else:
        return False