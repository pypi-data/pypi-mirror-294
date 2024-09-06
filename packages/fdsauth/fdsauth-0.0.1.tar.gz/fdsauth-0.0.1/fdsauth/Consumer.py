# Based on https://github.com/FIWARE/data-space-connector/blob/main/doc/deployment-integration/local-deployment/LOCAL.MD
import os
import requests


class Consumer:

    def __init__(self) -> None:
        self.protocol = os.environ.get("KEYCLOAK_PROTOCOL")
        self.keycloak_endpoint = os.environ.get("KEYCLOAK_ENDPOINT")
        self.keycloak_username = os.environ.get("KEYCLOAK_USERNAME")
        self.keycloak_password = os.environ.get("KEYCLOAK_PASSWORD")

    def get_auth_token(self):
        access_token = self.get_access_token()
        offer_uri = self.get_credential_offer_uri(access_token)
        pre_authorized_code = self.retrieve_actual_offer(access_token, offer_uri)
        credential_access_token = self.exchange_pre_authorized_code(pre_authorized_code)
        verifiable_credential = self.get_verifiable_credential(credential_access_token)

        return verifiable_credential

    # Get an AccessToken from Keycloak
    def get_access_token(self):
        url = "{PROTOCOL}://{KEYCLOAK_ENDPOINT}/realms/test-realm/protocol/openid-connect/token".format(
            PROTOCOL=self.protocol, KEYCLOAK_ENDPOINT=self.keycloak_endpoint
        )

        headers = {"Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "password",
            "client_id": "admin-cli",
            "username": self.keycloak_username,
            "password": self.keycloak_password,
        }

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            return access_token
        else:
            return None

    # Get a credential offer uri(for the `user-credential), using a retrieved AccessToken:
    def get_credential_offer_uri(self, access_token):
        url = "{PROTOCOL}://{KEYCLOAK_ENDPOINT}/realms/test-realm/protocol/oid4vc/credential-offer-uri?credential_configuration_id=user-credential".format(
            PROTOCOL=self.protocol, KEYCLOAK_ENDPOINT=self.keycloak_endpoint
        )

        headers = {"Authorization": "Bearer {}".format(access_token)}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("issuer") + response.json().get("nonce")
        else:
            return None

    # Use the offer uri(e.g. the issuerand nonce fields), to retrieve the actual offer:
    def retrieve_actual_offer(self, access_token, offer_uri):
        url = offer_uri

        headers = {"Authorization": "Bearer {}".format(access_token)}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return (
                response.json()
                .get("grants")
                .get("urn:ietf:params:oauth:grant-type:pre-authorized_code")
                .get("pre-authorized_code")
            )
        else:
            return None

    # Exchange the pre-authorized code from the offer with an AccessToken at the authorization server:
    def exchange_pre_authorized_code(self, pre_authorized_code):
        url = "{PROTOCOL}://{KEYCLOAK_ENDPOINT}/realms/test-realm/protocol/openid-connect/token".format(
            PROTOCOL=self.protocol, KEYCLOAK_ENDPOINT=self.keycloak_endpoint
        )

        headers = {"Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:pre-authorized_code",
            "code": pre_authorized_code,
        }

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            return access_token
        else:
            return None

    # Use the returned access token to get the actual credential:
    def get_verifiable_credential(self, credential_access_token):
        url = "{PROTOCOL}://{KEYCLOAK_ENDPOINT}/realms/test-realm/protocol/oid4vc/credential".format(
            PROTOCOL=self.protocol, KEYCLOAK_ENDPOINT=self.keycloak_endpoint
        )

        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(credential_access_token),
        }

        data = {
            "credential_identifier": "user-credential",
            "format": "jwt_vc",
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            verifiable_credential = response.json().get("credential")
            return verifiable_credential
        else:
            return None
