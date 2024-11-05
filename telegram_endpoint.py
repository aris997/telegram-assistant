import requests

def set(token, webhook) -> bool:
    URL = "https://api.telegram.org/bot{set_token}/setWebhook?url={webhook}/webhook"

    response = requests.get(URL.format(set_token=token, webhook=webhook))
    j_resp = response.json()
    # print(j_resp)

    if j_resp.get("ok", False):
        return j_resp["description"]
    else:
        return "not ok"

