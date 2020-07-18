from .base_url import BaseUrl
from ._exceptions import LimitTriesExceeded
from .request_errors import RequestErrors
from .rate_limit import RateLimit



class Spectator(BaseUrl):
    def __init__(self,region,token):
        super().__init__(region,token)

    def data_rq(self,url):
        self.rq_url=url
        data=self.rq.get(url)
        if data.status_code == 200:
            return data
        
        if data.status_code == 429:
            return RateLimit(data,self._rate_limit)

        return RequestErrors(data)



    def featured_game(self):
        url=f"{self.base_url}/lol/spectator/v4/featured-games?api_key={self.token}"
        return self.data_rq(url)


    def spect_summoner(self,Id):
        url=f"{self.base_url}/lol/spectator/v4/active-games/by-summoner/{Id}?api_key={self.token}"
        return self.data_rq(url)