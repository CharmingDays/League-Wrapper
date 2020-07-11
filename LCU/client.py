import requests as rq
import datetime,time
import asyncio,base64
import lcu_connector_python as lcu
import os,json





class BaseLCU(object):
    def __init__(self):
        self._local=lcu.connect()
        self.token=base64.b64encode(f'riot:{self._local["authorization"]}'.encode()).decode()
        self.url="https://"+self._local['url']
        self.headers={'Authorization':f"Basic {self.token}",'Accept': 'application/json'}
        self.session=rq.Session()
        self.session.verify=os.path.join(os.path.dirname(os.path.abspath(__file__)),'riotgames.pem')
        self.session.headers=self.headers
        # self.check_perm_file()



    def check_perm_file(self):
        perm_path=os.path.dirname(os.path.abspath(__file__)),'riotgames.pem'
        return perm_path


    
    def check_200(self,path,method:str,_bool:bool=False,payload=None):
        request_data=self.session.request(method,path,data=payload)
        
        if request_data.status_code in [200,204]:
            if _bool is True:
                return True
            return request_data

        raise RuntimeError



class Lobby(BaseLCU):
    def __init__(self):
        super().__init__()


    def create_lobby(self,queue_type:int=400):
        path=self.url+"/lol-lobby/v2/lobby"
        payload={
            "queueId": queue_type
        }
        return self.check_200(path,'POST',_bool=False,payload=json.dumps(payload))



    def role_position(self,primary="FILL",secondary="FILL"):
        url=self.url+"/lol-lobby/v2/lobby/members/localMember/position-preferences"
        payload={
            "firstPreference": primary,
            "secondPreference": secondary
        }
        position_data=self.session.put(url,data=json.dumps(payload))
        return position_data

    def send_invite(self,summoner_name:str):
        summoner_path=self.url+f"/lol-summoner/v1/summoners?name={summoner_name}"
        summoner_data=self.check_200(summoner_path)
        
        if summoner_data.status_code == 404:
            return f"Summoner {summoner_name} not found"
        
        summoner_id=summoner_data.json()['summonerId']
        invite_path=self.url+'/lol-lobby/v2/lobby/invitations'
        payload=[{
            "toSummonerId":summoner_id
        }]

        return self.check_200(invite_path,'POST',_bool=False,payload=json.dumps(payload))

    def leave_lobby(self):
        path=self.url+'/lol-lobby/v2/lobby'

        return self.check_200(path,'DELETE')


    def find_custom_games(self):
        path=self.url+'/lol-lobby/v1/custom-games'
        
        return self.check_200(path,'GET')


    def refresh_custom_games(self,return_refreshed:bool=False):
        path=self.url+'/lol-lobby/v1/custom-games/refresh'
        
        if return_refreshed is False:
            return self.check_200(path,'POST')
    
        if return_refreshed is True and self.check_200(path,'POST',_bool=True):
            return self.find_custom_games()


    
    def start_queue(self):
        path=self.url+'/lol-lobby/v2/lobby/matchmaking/search'

        return self.check_200(path,'POST')


    def stop_queue(self):
        path=self.url+'/lol-lobby/v2/lobby/matchmaking/search'

        return self.check_200(path,'DELETE')



class MatchMaking(BaseLCU):
    def __init__(self):
        super().__init__()


    def ready_check(self):
        """
        Check to see if lobby is in queue and ready to accept match
        """
        path=self.url+'/lol-matchmaking/v1/ready-check'
        return self.check_200(path,'GET')

    def decline_match(self):
        """
        Accept match found
        """
        path=self.url+'/lol-matchmaking/v1/ready-check/decline'
        
        return self.check_200(path,'POST')


    def accept_match(self):
        """
        Decline match found
        """
        path=self.url+'/lol-matchmaking/v1/ready-check/accept'
        
        return self.check_200(path,'POST')



