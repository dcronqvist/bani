import requests
import commands.api_requests as ar
import logging

@ar.use_token
def get_pihole_status_json():
    result = requests.get("https://api.dcronqvist.se/v1/pihole/status", headers={ "Authorization": ar.read_token() })
    return result.json()
    