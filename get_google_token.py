import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)

    print("\n\n====== COPY EVERYTHING BELOW INTO.streamlit/secrets.toml ======")
    print("[gmail]")
    print(f'token = "{creds.token}"')
    print(f'refresh_token = "{creds.refresh_token}"')
    print(f'client_id = "{creds.client_id}"')
    print(f'client_secret = "{creds.client_secret}"')
    print('type = "authorized_user"')
    print("==================================================================\n")

if __name__ == '__main__':
    main()