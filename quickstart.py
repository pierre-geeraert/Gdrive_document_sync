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

# [START drive_quickstart]

import credentials
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient import errors
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def update_file(service, file_id, new_name, new_description, new_mime_type,
            new_filename):
    """Update an existing file's metadata and content.

    Args:
        service: Drive API service instance.
        file_id: ID of the file to update.
        new_name: New name for the file.
        new_description: New description for the file.
        new_mime_type: New MIME type for the file.
        new_filename: Filename of the new content to upload.
        new_revision: Whether or not to create a new revision for this file.
    Returns:
        Updated file metadata if successful, None otherwise.
    """
    try:
        # First retrieve the file from the API.
        file = service.files().get(fileId=file_id).execute()

        # File's new metadata.
        file['name'] = new_name
        file['description'] = new_description
        file['mimeType'] = new_mime_type
        file['trashed'] = True

        # File's new content.
        media_body = MediaFileUpload(
            new_filename, mimetype=new_mime_type, resumable=True)

        # Send the request to the API.
        updated_file = service.files().update(
            fileId=file_id,
            body=file,
            media_body=media_body).execute()
        return updated_file
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None

def rename_file(service, file_id, new_title):
    file = {'title': new_title}
    updated_file = service.files().patch(
        fileId=file_id,
        body=file,
        fields='title').execute()
    return updated_file

def name_from_id(items,wanted_id):
    name = "No name found"
    for item in items:
        if item['id'] == wanted_id:
            name = item['name']
    return name

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
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
                credentials.google_credentials.source_account.location, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10,fields='nextPageToken, files(md5Checksum, id, name, mimeType,parents)').execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            name = item['name']
            parents = item['parents']
            id = item['id']
            print("--------------------------------------------")
            print("name: " + str(name))
            #print("parent: " + str(item['metadata']))
            print("id: " + str(id))
        #print(name_from_id(items,'1SsOvcrlpugMZK7uHXx6d0QsvsOtXj6i6'))
    #rename_file(service,'1AYdv1mGwEKSWlddYzAbbsfmywLXqAGgT','Certified2.PNG')
    #update_file(service,'1AYdv1mGwEKSWlddYzAbbsfmywLXqAGgT','Certified2.PNG',"description",None,None)
if __name__ == '__main__':
    main()
# [END drive_quickstart]
