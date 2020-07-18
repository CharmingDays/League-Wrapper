#TODO: requests.exceptions.ConnectionError
import requests



class BaseUrl(object):
    def __init__(self,region,token):
        self.region=region
        self.token=token
        self.base_url=f'https://{region}.api.riotgames.com'
        self.rq=requests
        self.rq_url=None


    def change_token(self,new_token):
        self.token=new_token
        return self.token


    def change_region(self,new_region):
        self.region=new_region
        return self.region

    @property
    def na1(self):
        self.region='na1'
    
    @property
    def kr(self):
        self.region='kr'
    
    @property
    def ru(self):
        self.region='ru'
    
    
    @property
    def jp(self):
        self.region='jp'
    
    @property
    def lan(self):
        self.region='lan'

    @property
    def lan2(self):
        self.region='lan2'

    @property
    def oce(self):
        self.region='oce'

    @property
    def oce2(self):
        self.region='oce2'

    @property
    def check_region(self):
        return self.region


    @property
    def check_token(self):
        return self.token

    @property
    def url(self):
        return self.rq_url