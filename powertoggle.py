import requests
import json

def power_toggle(tpLinkToken="0",deviceid="0", state=0):

    jsonpart1 = '{"method":"passthrough","params":{"deviceId":'
    jsonpart2 = '"' + deviceid + '"'
    jsonpart3 = ',"requestData":"{\\"system\\":{\\"set_relay_state\\":{\\"state\\":'
    jsonpart4 = str(state)
    jsonpart5 = '}}}"}}'

    apiendpoint = "https://use1-wap.tplinkcloud.com?token=" + tpLinkToken
    completejson = jsonpart1 + jsonpart2 + jsonpart3 + jsonpart4 + jsonpart5

    r = requests.post(url=apiendpoint, data=completejson)
    response = r.json()
    responsecode = response['error_code']
    return responsecode
