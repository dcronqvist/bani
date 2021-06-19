import requests
import commands.api_requests as ar
import logging

@ar.use_token
async def get_pihole_status_json(message):
    result = requests.get("https://api.dcronqvist.se/v1/pihole/status", headers={ "Authorization": ar.read_token() })
    j = result.json()
    status = j['status']
    mess = f"""
```json
{status['dns_queries_today']} DNS queries today, where {status['ads_blocked_today']} were towards ads. 
{round(status['ads_percentage_today'] * 10.0) / 10.0}% of all requests were towards ads.
```
"""
    await message.channel.send(mess)
    