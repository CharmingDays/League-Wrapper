import time


rate_limit={
    "second_use":20,
    "second":1,
    "minute_use":200,
    "minute":0,
    '200':True
}


def request_func():
    rate_limit['second_use']-=1
    rate_limit['minute_use']-=1

    return True

def request():
    while True:
        if rate_limit['200'] is False:
            return "Rate limit exceeded seconds"

        request_func()
        if rate_limit['second'] <1 and rate_limit['second_use'] <21:
            rate_limit['second']-=1
        if rate_limit['minute'] >= 200 and rate_limit['minute_use'] <201:
            rate_limit['minute']-=1



data=request()
print(data)