from .base_url import BaseUrl
from ._exceptions import LimitTriesExceeded
from .request_errors import RequestErrors
from .rate_limit import RateLimit



class Summoner(BaseUrl):
    def __init__(self,region,token,_rate_limit=None):
        super().__init__(region,token,_rate_limit)
        if _rate_limit is not None and _rate_limit > 25:
            raise LimitTriesExceeded

    
    def __repr__(self):
        return f"{self.region}"


    def data_rq(self,url):
        self.rq_url=url
        data=self.rq.get(url)
        if data.status_code == 200:
            return data
        
        if data.status_code == 429:
            return RateLimit(data,self._rate_limit)

        return RequestErrors(data)


    def summoner_id(self,accId):
        url=f"{self.base_url}/lol/summoner/v4/summoners/by-account/{accId}?api_key={self.token}"
        return self.data_rq(url)
    
    def summoner_name(self,name):
        url=f"{self.base_url}/lol/summoner/v4/summoners/by-name/{name}?api_key={self.token}"
        return self.data_rq(url)
    
    def summoner_puuid(self,puuid):
        url=f"{self.base_url}/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={self.token}"
        return self.data_rq(url)
    
    def summoner_accId(self,Id):
        url=f"{self.base_url}/lol/summoner/v4/summoners/{Id}?api_key={self.token}"
        return self.data_rq(url)