import json
import requests
from uuid import uuid4
from urllib.parse import urlencode

class BadRequest(Exception):
    pass


def format_graphql_json(post_json):
    data = post_json['data']['xdt_shortcode_media']

    if not data:
        raise BadRequest("This post does not exist")

    if not data['is_video']:
        raise BadRequest("This post is not a video")

    filename = f"{uuid4()}.mp4"
    width, height = data['dimensions']['width'], data['dimensions']['height']
    video_url = data['video_url']

    video_json = {
        "filename": filename,
        "width": str(width),
        "height": str(height),
        "videoUrl": video_url,
    }

    return video_json


def encode_post_request_data(shortcode):
    request_data = {
        "av": "0",
        "__d": "www",
        "__user": "0",
        "__a": "1",
        "__req": "3",
        "__hs": "19624.HYP:instagram_web_pkg.2.1..0.0",
        "dpr": "3",
        "__ccg": "UNKNOWN",
        "__rev": "1008824440",
        "__s": "xf44ne:zhh75g:xr51e7",
        "__hsi": "7282217488877343271",
        "__dyn": "7xeUmwlEnwn8K2WnFw9-2i5U4e0yoW3q32360CEbo1nEhw2nVE4W0om78b87C0yE5ufz81s8hwGwQwoEcE7O2l0Fwqo31w9a9x-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7-0iK2S3qazo7u1xwIw8O321LwTwKG1pg661pwr86C1mwraCg",
        "__csr": "gZ3yFmJkillQvV6ybimnG8AmhqujGbLADgjyEOWz49z9XDlAXBJpC7Wy-vQTSvUGWGh5u8KibG44dBiigrgjDxGjU0150Q0848azk48N09C02IR0go4SaR70r8owyg9pU0V23hwiA0LQczA48S0f-x-27o05NG0fkw",
        "__comet_req": "7",
        "lsd": "AVqbxe3J_YA",
        "jazoest": "2957",
        "__spin_r": "1008824440",
        "__spin_b": "trunk",
        "__spin_t": "1695523385",
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "PolarisPostActionLoadPostQueryQuery",
        "variables": json.dumps({
            "shortcode": shortcode,
            "fetch_comment_count": "null",
            "fetch_related_profile_media_count": "null",
            "parent_comment_count": "null",
            "child_comment_count": "null",
            "fetch_like_count": "null",
            "fetch_tagged_user_count": "null",
            "fetch_preview_comment_count": "null",
            "has_threaded_comments": "false",
            "hoisted_comment_id": "null",
            "hoisted_reply_id": "null",
        }),
        "server_timestamps": "true",
        "doc_id": "10015901848480474",
    }
    encoded = urlencode(request_data)
    return encoded


def fetch_from_graphql(post_id, timeout=0):
    if not post_id:
        return None

    api_url = "https://www.instagram.com/api/graphql"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-FB-Friendly-Name": "PolarisPostActionLoadPostQueryQuery",
        "X-CSRFToken": "RVDUooU5MYsBbS1CNN3CzVAuEP8oHB52",
        "X-IG-App-ID": "1217981644879628",
        "X-FB-LSD": "AVqbxe3J_YA",
        "X-ASBD-ID": "129477",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
    }

    encoded_data = encode_post_request_data(post_id)

    try:
        response = requests.post(api_url, headers=headers, data=encoded_data, timeout=timeout)
        response.raise_for_status()
        if response.json().get('statusText') == "error":
            return None
    except Exception as e:
        handle_scraper_error(e)
        return None

    if response.json().get('statusText') == "error":
        return None

    content_type = response.headers["content-type"]

    if content_type != "text/javascript; charset=utf-8":
        return None

    response_json = response.json()
    if not response_json.get('data'):
        return None

    formatted_json = format_graphql_json(response_json)
    return formatted_json