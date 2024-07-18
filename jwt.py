from pathlib import Path

import requests
import json

ACCESS_TOKEN_URL = "https://services.leadconnectorhq.com/oauth/token"
BASE_GET_CONTRACT_URL = "https://services.leadconnectorhq.com/contacts/"

CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
REFRESH_TOKEN = "REFRESH_TOKEN"
CONTACT_ID = "CONTACT_ID"


class JWTJsonWrapper:

    @staticmethod
    def create_or_write_json(json_data, file_name: str):
        contact_json_file = Path(f"{file_name}.json")
        if contact_json_file.exists():
            with open(contact_json_file, "r") as f:
                file = json.load(f)
        else:
            file = []
        file.append(json_data)
        with open(contact_json_file, "w") as f:
            json.dump(file, f, indent=4)


class JWTRequest:

    @staticmethod
    def get_jwt_token(
            client_id: str,
            client_secret: str,
            grant_type: str,
            user_type: str,
            redirect_uri: str | None = None,
            code: str | None = None,
            refresh_token: str | None = None,
    ):
        request = requests.post(
            ACCESS_TOKEN_URL,
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": grant_type,
                "user_type": user_type,
                "refresh_token": refresh_token,
                "code": code,
                "redirect_uri": redirect_uri,
            }
        )
        return request.json()

    @staticmethod
    def get_contact(
            token: str,
            contact_id: str,
            version: str = "2021-07-28"
    ):
        request = requests.get(
            BASE_GET_CONTRACT_URL + contact_id,
            data={"token": token},
            headers={
                "Authorization": f"Bearer {token}",
                "Version": version,
            },
        )
        return request.json()


if __name__ == "__main__":
    requester = JWTRequest()
    token = requester.get_jwt_token(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        grant_type="refresh_token",
        user_type="Company",
        refresh_token=REFRESH_TOKEN,
    )

    contact = requester.get_contact(
        token=token["access_token"],
        contact_id=CONTACT_ID,
    )

    JWTJsonWrapper.create_or_write_json(contact, "contacts")
    JWTJsonWrapper.create_or_write_json(token, "tokens")
