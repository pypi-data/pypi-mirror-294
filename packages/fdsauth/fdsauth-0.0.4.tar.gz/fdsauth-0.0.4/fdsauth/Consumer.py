import os
import requests
from requests.exceptions import RequestException


class Consumer:
    def __init__(self) -> None:
        """
        Initialize the Consumer class by retrieving the necessary credentials
        from environment variables. These credentials are required to authenticate
        and interact with the Keycloak server.

        Raises:
            ValueError: If any required environment variable is missing.
        """
        self.protocol = os.environ.get("KEYCLOAK_PROTOCOL")
        self.keycloak_endpoint = os.environ.get("KEYCLOAK_ENDPOINT")
        self.keycloak_username = os.environ.get("KEYCLOAK_USERNAME")
        self.keycloak_password = os.environ.get("KEYCLOAK_PASSWORD")

        # Ensure all required environment variables are provided
        if not all(
            [
                self.protocol,
                self.keycloak_endpoint,
                self.keycloak_username,
                self.keycloak_password,
            ]
        ):
            raise ValueError("Missing one or more required environment variables.")

        # Use a session to optimize HTTP connections
        self.session = requests.Session()

    def get_auth_token(self):
        """
        Orchestrates the process of retrieving a verifiable credential from the Keycloak server.
        This involves multiple steps including obtaining an access token, credential offer URI,
        exchanging pre-authorized codes, and finally retrieving the verifiable credential.

        Returns:
            str: The verifiable credential in `jwt_vc` format.

        Raises:
            Exception: If any of the intermediate steps fail.
        """
        try:
            access_token = self.get_access_token()
            offer_uri = self.get_credential_offer_uri(access_token)
            pre_authorized_code = self.retrieve_actual_offer(access_token, offer_uri)
            credential_access_token = self.exchange_pre_authorized_code(
                pre_authorized_code
            )
            verifiable_credential = self.get_verifiable_credential(
                credential_access_token
            )
            return verifiable_credential
        except Exception as e:
            raise Exception(f"Failed to obtain verifiable credential: {str(e)}")

    def get_access_token(self):
        """
        Obtains an OAuth2 access token from Keycloak using the username and password credentials.

        Returns:
            str: Access token if successful.

        Raises:
            RequestException: If the request fails.
        """
        url = f"{self.protocol}://{self.keycloak_endpoint}/realms/test-realm/protocol/openid-connect/token"

        headers = {"Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "password",
            "client_id": "admin-cli",
            "username": self.keycloak_username,
            "password": self.keycloak_password,
        }

        try:
            response = self.session.post(url, headers=headers, data=data)
            response.raise_for_status()  # Raises HTTPError if status code is not 200
            access_token = response.json().get("access_token")
            if not access_token:
                raise ValueError("Access token not found in response.")
            return access_token
        except RequestException as e:
            raise RequestException(f"Failed to get access token: {str(e)}")

    def get_credential_offer_uri(self, access_token):
        """
        Retrieves the credential offer URI using a valid access token.

        Args:
            access_token (str): The access token obtained from Keycloak.

        Returns:
            str: The credential offer URI, constructed from issuer and nonce.

        Raises:
            RequestException: If the request fails.
        """
        url = f"{self.protocol}://{self.keycloak_endpoint}/realms/test-realm/protocol/oid4vc/credential-offer-uri"
        url += "?credential_configuration_id=user-credential"

        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            issuer = response_data.get("issuer")
            nonce = response_data.get("nonce")
            if not issuer or not nonce:
                raise ValueError("Issuer or nonce missing in response.")
            return f"{issuer}{nonce}"
        except RequestException as e:
            raise RequestException(f"Failed to get credential offer URI: {str(e)}")

    def retrieve_actual_offer(self, access_token, offer_uri):
        """
        Retrieves the actual credential offer from the provided offer URI.

        Args:
            access_token (str): The access token obtained from Keycloak.
            offer_uri (str): The credential offer URI.

        Returns:
            str: Pre-authorized code.

        Raises:
            RequestException: If the request fails.
        """
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = self.session.get(offer_uri, headers=headers)
            response.raise_for_status()
            grants = response.json().get("grants")
            if not grants:
                raise ValueError("Grants not found in response.")
            pre_authorized_code = grants.get(
                "urn:ietf:params:oauth:grant-type:pre-authorized_code", {}
            ).get("pre-authorized_code")
            if not pre_authorized_code:
                raise ValueError("Pre-authorized code not found.")
            return pre_authorized_code
        except RequestException as e:
            raise RequestException(f"Failed to retrieve actual offer: {str(e)}")

    def exchange_pre_authorized_code(self, pre_authorized_code):
        """
        Exchanges the pre-authorized code for an access token to obtain a verifiable credential.

        Args:
            pre_authorized_code (str): The pre-authorized code.

        Returns:
            str: Credential access token.

        Raises:
            RequestException: If the request fails.
        """
        url = f"{self.protocol}://{self.keycloak_endpoint}/realms/test-realm/protocol/openid-connect/token"

        headers = {"Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:pre-authorized_code",
            "code": pre_authorized_code,
        }

        try:
            response = self.session.post(url, headers=headers, data=data)
            response.raise_for_status()
            access_token = response.json().get("access_token")
            if not access_token:
                raise ValueError("Credential access token not found.")
            return access_token
        except RequestException as e:
            raise RequestException(f"Failed to exchange pre-authorized code: {str(e)}")

    def get_verifiable_credential(self, credential_access_token):
        """
        Retrieves the actual verifiable credential using the credential access token.

        Args:
            credential_access_token (str): The access token specific to the credential.

        Returns:
            str: The verifiable credential in JWT format.

        Raises:
            RequestException: If the request fails.
        """
        url = f"{self.protocol}://{self.keycloak_endpoint}/realms/test-realm/protocol/oid4vc/credential"

        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {credential_access_token}",
        }

        data = {
            "credential_identifier": "user-credential",
            "format": "jwt_vc",
        }

        try:
            response = self.session.post(url, headers=headers, json=data)
            response.raise_for_status()
            verifiable_credential = response.json().get("credential")
            if not verifiable_credential:
                raise ValueError("Verifiable credential not found.")
            return verifiable_credential
        except RequestException as e:
            raise RequestException(
                f"Failed to retrieve verifiable credential: {str(e)}"
            )

    def __del__(self):
        """
        Ensures that the session is properly closed when the object is destroyed.
        """
        self.session.close()
