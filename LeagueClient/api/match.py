from .base_url import BaseUrl
from ._exceptions import LimitTriesExceeded
from .request_errors import RequestErrors
from .rate_limit import RateLimit
from .utils_data import champs,seasons,queue_types

__all__=["Match"]
class MatchInfo(object):
    def __init__(self,data):
        self.data=data
        self.json_data=data.json()

    def __repr__(self):
        return str(self.data.status_code)

    @property
    def match_ids(self):
        data_json=self.data.json()
        new_ids=[]
        for match in data_json['matches']:
            new_ids.append(match['gameId'])

        return new_ids

    @property
    def champions(self):
        champion_sets={}
        for match in self.json_data['matches']:
            champion_sets[champs['reversed_order'][match['champion']]]=match['champion']
        _reversed={v: k for k, v in champion_sets.items()}

        return champion_sets,_reversed

    @property
    def champion_ids(self):
        champ_ids=[]
        for match in self.json_data['matches']:
            champ_ids.append(match['champion'])

        return champ_ids

    @property
    def champion_names(self):
        champ_names=[]
        for match in self.json_data['matches']:
            champ_names.append(champs['reversed_order'][match['champion']])
        
        return champ_names

    
    @property
    def queue_types(self):
        queues=[]
        for match in self.json_data['matches']:
            queues.append(match['queue'])
        
        return queues

    @property
    def json(self):
        return self.json_data
    
    @property
    def raw_data(self):
        return self.data

    @property
    def status_code(self):
        return self.data.status_code
    



class Match(BaseUrl):
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
            champion=self._champion_check(opts['champion'])
            new_link+=champion
            opts.pop('champion')

        if 'queue' in opts:
            queue=self._queue_check(opts['queue'])
            new_link+=queue
            opts.pop('queue')

        if 'season' in opts:
            season=self._season_check(opts['season'])
            new_link+=season
            opts.pop('season')
            
        for key in opts:
            new_link+=f"&{key}={opts[key]}"

        return new_link

    def get_matches(self,accId,**opts):
        options=['champion','queue','season','endTime','beginTime','endIndex','beginIndex']
        url=f"{self.base_url}/lol/match/v4/matchlists/by-account/{accId}?api_key={self.token}"
        for op in opts.copy():
            if op not in options:
                opts.pop(op)
                print(f'Keyword "{op}" not found. Removed')

        new_url=self.check_all_opts(opts)
        data=self.data_rq(url+new_url)
        return MatchInfo(data)
