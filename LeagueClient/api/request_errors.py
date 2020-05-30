class RequestErrors(object):
    def __init__(self,data):
        self.data=data


    def __repr__(self):
        return str(self.data.status_code)

    @property
    def json(self):
        return self.data.json()


    @property
    def text(self):
        return self.data.text

    @property
    def url(self):
        return self.data.url