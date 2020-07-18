from .api.base_url import BaseUrl
from .api.champion import ChampionMastery as _ChampionMastery
from .api.clash import Clash as _Clash
from .api.league import LeagueRank as _LeagueRank
from .api.match import Match as _Match
from .api.rate_limit import RateLimit as _RateLimit
from .api.request_errors import RequestErrors as _RequestErrors
from .api.spectator import Spectator as _Spectator
from .api.summoner import Summoner as _Summoner
from .api.utils import Utils as _Utils

class Client(BaseUrl):
    def __init__(self,region,token):
        super().__init__(region,token)

    @property
    def Summoner(self):
        return _Summoner(region=self.region,token=self.token,_rate_limit=self.rate_limit)


    @property
    def ChampionMastery(self):
        return _ChampionMastery(region=self.region,token=self.token,_rate_limit=self.rate_limit)


    @property
    def Clash(self):
        return _Clash(region=self.region,token=self.token,_rate_limit=self.rate_limit)


    @property
    def LeagueRank(self):
        return _LeagueRank(region=self.region,token=self.token,_rate_limit=self.rate_limit)


    @property
    def Match(self):
        return _Match(region=self.region,token=self.token,_rate_limit=self.rate_limit)


    @property
    def RateLimit(self):
        return _RateLimit(region=self.region,token=self.token,_rate_limit=self.rate_limit)


    @property
    def Spectator(self):
        return _Spectator(region=self.region,token=self.token,_rate_limit=self.rate_limit)


    @property
    def Utils(self):
        return _Utils(region=self.region,token=self.token,_rate_limit=self.rate_limit)

