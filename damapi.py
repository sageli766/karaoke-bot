import aiohttp
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

TOP_CHART_URL = os.getenv('TOP_CHART_URL')
SEARCH_KEYWORD_URL = os.getenv('SEARCH_KEYWORD_URL')
USERCODE = os.getenv('USERCODE')
AUTHKEY = os.getenv('AUTHKEY')
AUTHTOKEN = os.getenv('AUTHTOKEN')

async def get_song_info(response_json):
    songs = response_json.get('list', [])
    song_info_list = []
    for song in songs:
        title = song.get('title', '')
        artist = song.get('artist', '')
        song_info_list.append((title, artist))
    
    logger.debug(song_info_list)

    return {
        'songs': song_info_list,
        'pageCount': response_json.get('data', {}).get('pageCount', 0),
        'pageNo': response_json.get('data', {}).get('pageNo', 0),
        'totalCount': response_json.get('data', {}).get('totalCount', 0)
    }

# url = TOP_CHART_URL
# headers = {
#     'Content-Type': 'application/json; charset=UTF-8',
#     'format': 'json'
# }
# data = {
#     'compId': 1,
#     'userCode': USERCODE,
#     'authToken': AUTHTOKEN,
#     'compAuthKey': AUTHKEY,
#     'dispNumber': 30,
#     'pageNo': 1,
#     'targetContractId': 1,
#     'musicViewsRankingId': 2585,
#     'serviceId': 1,
#     'deviceId': 141,
#     'getCount': 200,
#     'thumbnailType': 1
# }

async def search_by_keyword(keyword, disp_count, page_no):
    url = SEARCH_KEYWORD_URL
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'format': 'json'
    }
    data = {
        'authKey': AUTHKEY,
        'compId': "1",
        'dispCount': disp_count,
        'keyword': keyword,
        'minseiModelNum': "M1",
        'modelPatternCode': "0",
        'modelTypeCode': "2",
        'pageNo': page_no,
        'shopType': "02",
        'sort': "2",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                logger.error("Error: %d", response.status)