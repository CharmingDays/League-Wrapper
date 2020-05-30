from .base_url import BaseUrl
from ._exceptions import LimitTriesExceeded
from .request_errors import RequestErrors
from .rate_limit import RateLimit
from .utils_data import champs,seasons,queue_types



class Match(BaseUrl):
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
    

    def match_info(self,matchId):
        url=f"{self.base_url}/lol/match/v4/matches/{matchId}?api_key={self.token}"
        return self.data_rq(url)


    def match_timelines(self,matchId):
        url=f"{self.base_url}/lol/match/v4/timelines/by-match/{matchId}?api_key={self.token}"
        return self.data_rq(url)
    
    
    def tournaments(self,tournamentCode):
        url=f"{self.base_url}/lol/match/v4/matches/by-tournament-code/{tournamentCode}/ids?api_key={self.token}"
        return self.data_rq(url)

    def tournament_match(self,matchId,tournamentCode):
        url=f"{self.base_url}/lol/match/v4/matches/{matchId}/by-tournament-code/{tournamentCode}?api_key={self.token}"
        return self.data_rq(url)

    def _champion_check(self,_champs):
        new_champs=''
        for champ in _champs.copy():
            if champ not in champs['champion_ids']:
                _champs.remove(champ)

            else:
                new_champs+=f'&champion={champ}'
        
        if not _champs:
            return "&champion="


        return new_champs



    def _season_check(self,_seasons):
        new_seasons=''
        for season in _seasons.copy():
            if season not in seasons['season_ids']:
                _seasons.remove(season)
            else:
                new_seasons+=f'&season={season}'
        
        if not _seasons:
            return "&season="

        return new_seasons


    def _queue_check(self,_queues):
        new_queues=''
        for queue in _queues.copy():
            if queue not in queue_types['queue_ids']:
                _queues.remove(queue)
            else:
                new_queues+=f'&queue={queue}'

        if not _queues:
            return "&queue="
        
        return new_queues

    def check_all_opts(self,opts):
        new_link=""
        if 'champion' in opts:
            champion=_champion_check(opts['champion'])
            new_link+=champion
            opts.pop('champion')

        if 'queue' in opts:
            queue=_queue_check(opts['queue'])
            new_link+=queue
            opts.pop('queue')

        if 'season' in opts:
            season=_season_check(opts['season'])
            new_link+=season
            opts.pop('season')
            
        for key in opts:
            new_link+=f"&{key}={opts[key]}"

        return new_link

    def _match_opts(self,accId,**opts):
        options=['champion','queue','season','endTime','beginTime','endIndex','beginIndex']
        url=f"{self.base_url}/lol/match/v4/matchlists/by-account/{accId}?api_key={self.token}"
        for op in opts.copy():
            if op not in options:
                opts.pop(op)
                print(f'Keyword "{op}" not found. Removed')

        new_url=check_all_opts(opts)
        return self.data_rq(url+new_url)
