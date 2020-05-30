from .base_url import BaseUrl
from ._exceptions import LimitTriesExceeded
from .request_errors import RequestErrors
from .rate_limit import RateLimit



class LeagueRank(BaseUrl):
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

    

    def challenger_ranks(self,queue_type):
        url=f'{self.base_url}/lol/league/v4/challengerleagues/by-queue/{queue_type}?api_key={self.token}'
        return self.data_rq(url)

    def summoner_rank(self,Id):
        url=f"{self.base_url}/lol/league/v4/entries/by-summoner/{Id}?api_key={self.token}"
        return self.data_rq(url)

    def league_entries(self,queue_type,tier,division):
        url=f"{self.base_url}/lol/league/v4/entries/{queue_type}/{tier}/{division}?api_key={self.token}"
        return self.data_rq(url)


    def grandmaster_ranks(self,queue_type):
        url=f"{self.base_url}/lol/league/v4/grandmasterleagues/by-queue/{queue_type}?api_key={self.token}"
        return self.data_rq(url)

    def master_ranks(self,queue_type):
        url=f"{self.base_url}/lol/league/v4/masterleagues/by-queue/{queue_type}?api_key={self.token}"

    def leagues(self,leagueId):
        url=f"{self.base_url}/lol/league/v4/leagues/{leagueId}?api_key={self.token}"
        return self.data_rq(url)

