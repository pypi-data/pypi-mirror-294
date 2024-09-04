import json
import logging

import boto3
import pytest

from pysll import Constellation


@pytest.fixture(scope="session")
def client():
    """Helper function to retrieve an actively logged in client.

    This uses AWS secrets manager to retrieve credentials.  If you do
    not have access to ECL'S AWS secrets manager, you must override this
    function in order to run the tests.
    """

    # Now, get an auth token by logging into constellation for each environment
    client = Constellation(host="https://constellation-stage.emeraldcloudlab.com")
    try:
        with open("./.auth") as handle:
            auth_token, notebook_id = handle.read().strip().split("\n")
    except FileNotFoundError:
        secrets_client = boto3.session.Session().client(service_name="secretsmanager")  # type: ignore
        credentials_secret = secrets_client.get_secret_value(SecretId="manifold-service-user-constellation-credentials")
        credentials_dict = json.loads(credentials_secret["SecretString"])
        username = credentials_dict["username"]
        password = credentials_dict["password"]
        client.login(username, password)
    else:
        logging.warning("Loaded credentials from .auth file")
        client._auth_token = auth_token
        client._notebook_id = notebook_id

    return client
