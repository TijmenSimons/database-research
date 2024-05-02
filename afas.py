import base64
import json
import logging
import requests


TOKEN = "<token><version>1</version><data>05D62C6E304F4E2AB1B8A0AB5B822992F9DDDA7176814B398FC22092CA0D32E9</data></token>"
token = base64.b64encode(TOKEN.encode("ascii")).decode("ascii")
environment = 89523


def afas_get(
    token: str,
    environment: str,
    connector: str,
    skip: int = -1,
    take: int = -1,
    url: str = None
):
    if not url:
        url = "https://{}.resttest.afas.online/ProfitRestServices/{}{}".format(
            environment, connector, f"?skip={skip}&take={take}"
        )

    headers = {
        "authorization": f"AfasToken {token}",
        "content-type": "application/json",
    }

    response = requests.get(url=url, headers=headers)

    if response.status_code == 401:
        raise Exception("Token is not valid")

    if response.status_code == 200:
        response_data = response.json()
        return response_data
    
    if response.status_code == 400:
        with open("output.html", "w") as f:
            f.write(response.content.decode("utf-8"))
        return None
    
    print(response.__dict__)
    print(response.content.decode("utf-8"))

    raise exit("ERROR Something went wrong")


def afas_post(
    data: list[dict],
    token: str,
    environment: str,
    connector: str,
):
    for i in data:
        new_data = {connector: {"Element": {"Fields": i}}}
        json_data = json.dumps(new_data)
        url = "https://{}.resttest.afas.online/ProfitRestServices/connectors/{}".format(
            environment, connector
        )
        headers = {
            "authorization": f"AfasToken {token}",
            "content-type": "application/json",
        }

        logging.info(json_data)
        response = requests.post(url=url, data=json_data, headers=headers)

        if response.status_code == 401:
            raise Exception("Token is not valid")
        if response.status_code != 200 | 201:
            raise Exception("Something went wrong")
    return response.json()


def get_metainfo(connector: str):
    return afas_get(
        token,
        environment,
        "",
        url=f"https://connect.afas.nl/afasrest/UpdateConnectorMetaInfo?connectorid={connector}?skip=-1&take=-1"
    )


all_connectors = {
    "updateConnectors": [
        {"id": "KnUser", "description": "Gebruiker"},
        {"id": "PtRealization", "description": "Nacalculatie"},
        {"id": "KnOrganisation", "description": "Organisatie"},
    ],
    "getConnectors": [
        {"id": "Urenontrafelaar_Contacten", "description": "Urenontrafelaar_Contacten"},
        {"id": "Urenontrafelaar_Feestdagen", "description": "Urenontrafelaar_Feestdagen"},
        {"id": "Urenontrafelaar_Organisaties", "description": "Urenontrafelaar_Organisaties"},
        {"id": "Urenontrafelaar_Reisuren", "description": "Urenontrafelaar_Reisuren"},
        {"id": "Urenontrafelaar_Urensoorten_Reisuren", "description": "Urenontrafelaar_Urensoorten_Reisuren"},
        {"id": "vSync_Gebruikers", "description": "vSync_Gebruikers"},
    ],
    "info": {
        "envid": "T89523AD",
        "appName": "VSync",
        "group": "Alle Profit-gebruikers (89523.tsi)",
        "tokenExpiry": "0",
    },
}


def main():
    res = get_metainfo("PtRealization")
    print(res)


if __name__ == "__main__":
    main()
