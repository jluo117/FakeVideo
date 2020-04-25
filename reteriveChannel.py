import requests
from bs4 import BeautifulSoup as bs
def get_video_info(url):
    # download HTML code
    myUrl = "https://www.youtube.com/watch?v="+url
    print(myUrl)
    content = requests.get(myUrl)


    # create beautiful soup object to parse HTML
    soup = bs(content.content, "html.parser")
    if soup == None:
        return None
    # initialize the result
    result = {}
    channel_tag = soup.find("div", attrs={"class": "yt-user-info"}).find("a")
    channel_url = f"https://www.youtube.com{channel_tag['href']}"
    channel_name = channel_tag.text
    #esult['channel'] = {'name': channel_name, 'url': channel_url}
    return channel_name
