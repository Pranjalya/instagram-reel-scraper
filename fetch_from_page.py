import requests
from bs4 import BeautifulSoup

def get_video_data(url):
    try:
        headers = {
            "accept": "*/*",
            "host": "www.instagram.com",
            "referer": "https://www.instagram.com/",
            "DNT": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        video_tag = soup.find('video')

        if video_tag:
            print(video_tag.keys())
            video_data = {
                'src': video_tag.get('src', ''),
                'width': video_tag.get('width', ''),
                'height': video_tag.get('height', ''),
                'type': video_tag.get('type', ''),
                'controls': video_tag.get('controls', ''),
            }
            return video_data
        else:
            print("No <video> tag found on the page.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the HTML page: {e}")
        return None


if __name__=="__main__":
    url = 'https://www.instagram.com/p/C1PexXQCk7P'
    video_data = get_video_data(url)
    if video_data:
        print("Video Data:")
        for key, value in video_data.items():
            print(f"{key}: {value}")
