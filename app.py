import re
from fetch_from_graphql import fetchFromGraphQL
from fetch_from_page import fetchFromPage

def getPostId(postUrl):
    post_regex = re.compile(r'^https://(?:www\.)?instagram\.com\/p\/([a-zA-Z0-9_-]+)\/?')
    reel_regex = re.compile(r'^https:\/\/(?:www\.)?instagram\.com\/reels?\/([a-zA-Z0-9_-]+)\/?')
    post_id = None

    if not postUrl:
        raise Exception("Instagram URL was not provided")

    post_check = post_regex.match(postUrl)
    if post_check:
        post_id = post_check.group(1)

    reel_check = reel_regex.match(postUrl)
    if reel_check:
        post_id = reel_check.group(1)

    if not post_id:
        raise Exception("Instagram post/reel ID was not found")

    return post_id


async def fetchPostJson(postUrl, timeout=None):
    post_id = getPostId(postUrl)

    page_json = await fetchFromPage(post_id, timeout)
    if page_json:
        return page_json

    api_json = await fetchFromGraphQL(post_id, timeout)
    if api_json:
        return api_json

    raise Exception("Video link for this post is not public.", 401)
