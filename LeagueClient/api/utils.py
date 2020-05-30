from .base_url import BaseUrl
from ._exceptions import LimitTriesExceeded
from .request_errors import RequestErrors
from .rate_limit import RateLimit




class Utils(BaseUrl):
    def __init__(self,region,token,_rate_limit=None):
        super().__init__(region,token,_rate_limit)
        if _rate_limit is not None and _rate_limit > 25:
            raise LimitTriesExceeded



    def data_rq(self,url):
        self.rq_url=url
        data=self.rq.get(url)
        if data.status_code == 200:
            return data
        
        if data.status_code == 429:
            return RateLimit(data,self._rate_limit)

        return RequestErrors(data)
    

    def game_status(self,region=None):
        if region is not None:
            self.change_region(new_region=region)

        url=f"{self.base_url}/lol/status/v3/shard-data?api_key={self.token}"
        return self.data_rq(url)


    def third_party_code(self,Id):
        url=f"{self.base_url}/lol/platform/v4/third-party-code/by-summoner/{Id}?api_key={self.token}"
        return self.data_rq(url)


