from mitmproxy import http
from loguru import logger
from karaoke import *

class InterceptRequests:

    async def request(self, flow: http.HTTPFlow) -> None: 
        if flow.request.method == "POST" and "csgw.clubdam.com/cwa/win/minsei/music/playLog/GetMusicStreamingURL.api" in flow.request.pretty_url:
            get_current_session().update_new_song_playing(True)
            get_current_session().update_results_shown(False)
            logger.info("Intercepted request to GetMusicStreamingURL.api, new_song_playing set to True, results_shown set to False")
        elif flow.request.method == "POST" and "csgw.clubdam.com/cwa/win/minsei/scoring/RegisterMinScoringAi.api" in flow.request.pretty_url:
            get_current_session().update_new_song_playing(False)
            get_current_session().update_results_shown(True)
            logger.info("Detected scoring register request. new_song_playing set to False, results_shown set to True")
            print("JSON request data:", flow.request.text)

addons = [
    InterceptRequests()
]

# async def start_proxy():
#     from mitmproxy.tools.main import mitmdump
#     import sys

#     logger.info("Starting proxy...")
#     mitmdump(['-s', __file__, '--quiet'])

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(start_proxy())