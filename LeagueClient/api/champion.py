from .base_url import BaseUrl
from ._exceptions import LimitTriesExceeded
from .request_errors import RequestErrors
from .rate_limit import RateLimit

__all__=["ChampionMastery"]

class ChampionMastery(BaseUrl):
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


    def all_champ_mastery(self,Id):
        url=f'{self.base_url}/lol/champion-mastery/v4/champion-masteries/by-summoner/{Id}?api_key={self.token}'
        return self.data_rq(url)


    def champ_mastery(self,Id,champId):
        url=f'{self.base_url}/lol/champion-mastery/v4/champion-masteries/by-summoner/{Id}/by-champion/{champId}?api_key={self.token}'
        return self.data_rq(url)


    def total_mastery(self,Id):
        url=f'{self.base_url}/lol/champion-mastery/v4/scores/by-summoner/{Id}?api_key={self.token}'
        return self.data_rq(url)



    def champion_rotations(self):
        url=f'{self.base_url}/lol/platform/v3/champion-rotations?api_key={self.token}'
        return self.data_rq(url)

