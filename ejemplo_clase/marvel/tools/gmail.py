#!/usr/bin/python3
import pickle
import os
import base64

from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Gmail():
    def __init__(self, client_secret_file):
        # Scopes:
        # https://developers.google.com/workspace/guides/identify-scopes
        scopes = [
            'https://mail.google.com/'
        ]
        try:
            self.service = self.__create_service(client_secret_file, scopes)
        except:
            print("Gmail service not created")
            self.service = None

    @staticmethod
    def __create_service(client_secret_file, *scopes, api_name="gmail", api_version="v1"):
        print(client_secret_file, api_name, api_version, scopes, sep='-')
        CLIENT_SECRET_FILE = client_secret_file
        API_SERVICE_NAME = api_name
        API_VERSION = api_version
        SCOPES = [scope for scope in scopes[0]]
        print(SCOPES)

        cred = None

        base_path = os.path.dirname(os.path.realpath(client_secret_file))
        pickle_file = os.path.join(base_path, f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle')
        print("gmail file localtion:", pickle_file)

        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server()

            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
            print(API_SERVICE_NAME, 'service created successfully')
            return service
        except Exception as e:
            print('Unable to connect.')
            print(e)
            return None


    def send_mail(self, title, message, to_email_list):
        if self.service is None:
            print("Error: Gmail service not created")
            return

        mime_msg = MIMEText(message)
        mime_msg['to'] = ",".join(to_email_list)
        mime_msg['subject'] = title
        raw_string = {'raw': base64.urlsafe_b64encode(mime_msg.as_string().encode()).decode()}

        res = self.service.users().messages().send(userId="me", body=raw_string).execute()


if __name__ == "__main__":
    gmail = Gmail("client_secret.json")

    # gmail.send_mail("Probando", "mi mensaje", ["hhvservice@gmail.com"])