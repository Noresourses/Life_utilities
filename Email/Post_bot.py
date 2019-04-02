# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gmail_quickstart]
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from apiclient import errors
import requests
from pprint import pprint
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def sanitize_data(file_data:str) -> list:
    data = []
    split_data = file_data.splitlines()
    pprint(split_data)
    for line in split_data:
        if len(line) == 1:
            continue

        elif len(line.split()) == 1:
            print(line,'date')
        else:
            print('data', line)

            sl = line.split()

            data.append({"SID": sl[0], "FAULT": sl[1], "VBAT": sl[2], "TEMPBAT": sl[3], "TEMP": sl[4], "PRES": sl[5], "HUMID": sl[6], "RAIN": sl[7],
             "TEMPSHT21": sl[8], "HUMSHT21": sl[9]})



    return data

def post_data(data_list: list)-> None:
    url = 'http://localhost:3000/streams/add/5ca351e8869f706d16498f05'
    headers ={
        'apikey': 'supersecretkey',
        'Content-Type': 'application/json'
    }

    data ={'data': data_list}

    r = requests.post(url, data=json.dumps(data), headers=headers)
    pprint(r.content)

    pass

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    messages = service.users().messages().list(userId='me').execute()
    print(messages)
    for message in messages['messages']:

        #print(message)
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = msg['payload']

        for part in payload['parts']:
            if part['filename']:
                if 'data' in part['body']:
                    data = part['body']['data']
                else:
                    att_id = part['body']['attachmentId']
                    att = service.users().messages().attachments().get(userId='me', messageId=message['id'],
                                                                       id=att_id).execute()
                    data = att['data']
                #todo: these are the attachments
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8')).decode("utf-8")

                print(file_data )
                sf_data = sanitize_data(file_data)

                post_data(sf_data)
                return
                #path = prefix + part['filename']

        #print(parts['headers'])
        print('-----------------')
        print('From: ', [x for x in payload['headers'] if x['name'] == 'From'])
        print('To: ',[x for x in payload['headers'] if x['name'] == 'Delivered-To'])


        pass


    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])


def GetAttachments(service, user_id, msg_id, store_dir=""):
    """Get and store attachment from Message with given id.
        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
                can be used to indicate the authenticated user.
            msg_id: ID of Message containing attachment.
            store_dir: The directory used to store attachments.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        parts = [message['payload']]
        while parts:
            part = parts.pop()
            if part.get('parts'):
                parts.extend(part['parts'])
            if part.get('filename'):
                if 'data' in part['body']:
                    file_data = base64.urlsafe_b64decode(part['body']['data'].encode('UTF-8'))
                elif 'attachmentId' in part['body']:
                    attachment = service.users().messages().attachments().get(
                        userId=user_id, messageId=message['id'], id=part['body']['attachmentId']
                    ).execute()
                    file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                else:
                    file_data = None
                if file_data:
                    #do some staff, e.g.
                    path = ''.join([store_dir, part['filename']])
                    with open(path, 'w') as f:
                        f.write(file_data)
    except Exception as error:
        print ('An error occurred: %s' % error)



if __name__ == '__main__':
    main()
# [END gmail_quickstart]