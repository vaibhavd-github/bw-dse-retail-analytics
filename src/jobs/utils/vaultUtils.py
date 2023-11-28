# feature/job1
import requests 

VAULT_URL = "http://127.0.0.1:8200"
ROLE_ID = "865df005-e0c3-42c9-8ceb-883f3e88c8fd"
SECRET_ID = "87a07373-6f46-8651-2aab-49fb62154557"
SECRET_PATH = "secret/data/snow"

def authenticate_with_approle():
    auth_url = f"{VAULT_URL}/v1/auth/approle/login"
    auth_data = {
        "role_id": ROLE_ID,
        "secret_id": SECRET_ID
    }
    try:
        auth_response = requests.post(auth_url, json=auth_data)
        auth_response.raise_for_status()
        token = auth_response.json()["auth"]["client_token"]
        print("token===========", token)
        return token
    except requests.exceptions.RequestException as e:
        print(f"Authentication error: {e}")
        return None

def get_secret(token):
    headers = {
        "X-Vault-Token": token,
    }
    url = f"{VAULT_URL}/v1/{SECRET_PATH}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        secret_data = response.json()["data"]
        return secret_data
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving secret: {e}")
        return None

# Example usage
token = authenticate_with_approle()
if token:
    secret = get_secret(token)
    if secret:
        print("Retrieved secret data:", secret)


token= authenticate_with_approle()
secret_data= get_secret(token)

print(secret_data)
