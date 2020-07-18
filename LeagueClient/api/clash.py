from .base_url import BaseUrl
from ._exceptions import LimitTriesExceeded
from .request_errors import RequestErrors
from .rate_limit import RateLimit



class Clash(BaseUrl):
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



    def get_player(self,Id):
        url=f"{self.base_url}/lol/clash/v1/players/by-summoner/{Id}?api_key={self.token}"
        return self.data_rq(url)


    def get_team(self,teamId):
        url=f"{self.base_url}/lol/clash/v1/teams/{teamId}?api_key={self.token}"
        return self.data_rq(url)

    def tournament_events(self):
        url=f"{self.base_url}/lol/clash/v1/tournaments?api_key={self.token}"
        return self.data_rq(url)


    
    def tournament_teamId(self,teamId):
        url=f"{self.base_url}/lol/clash/v1/tournaments/by-team/{teamId}?api_key={self.token}"
        return self.data_rq(url)

    def tournament_Id(self,tourId):
        url=f"{self.base_url}/lol/clash/v1/tournaments/{tourId}?api_key={self.token}"
        return self.data_rq(url)


    