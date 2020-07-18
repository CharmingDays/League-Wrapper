import requests, asyncio
import time




class RequestData(object):
    def __init__(self,request_object):
        self.rq_data=request_object
        self._prepare_class()

    def _prepare_class(self):
        self._okay_data


    @property
    def okay(self):
        okay_codes=[200]
        if self.rq_data.status_code in okay_codes:
            setattr(self,'json_data',self.rq_data.json())
            return True

        return False


    def json(self):
        if hasattr(self,'json_data'):
            return self.json_data

        return self.rq_data.json()




