#from https://bits.mdminhazulhaque.io/python/rename-list-of-files-in-google-drive-using-python.html
from __future__ import print_function
import httplib2
import os
import json

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import file

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials_source.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'credentials_source.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def rename_file(service, file_id, new_title):
    try:
        file = {'title': new_title}
        updated_file = service.files().patch(
            fileId=file_id,
            body=file,
            fields='title').execute()
        return updated_file
    except:
        print('An error occurred')
        return None


def list_files_in_folder(service, folder_id):
    files = []
    page_token = None

    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            children = service.children().list(folderId=folder_id, **param).execute()
            for child in children.get('items', []):
                files.append(child['id'])
            page_token = children.get('nextPageToken')
            if not page_token:
                break
        except:
            print('An error occurred')
            break
    return files


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)

    for fileid in list_files_in_folder(service, '1SsOvcrlpugMZK7uHXx6d0QsvsOtXj6i6'):
        try:
            file = service.files().get(fileId=fileid).execute()
            if (file['title'].startswith('Copy of ')):
                new_title = file['title'].replace('Copy of ', 'not ')
                rename_file(service, fileid, new_title)
        except:
            print('An error occurred')


if __name__ == '__main__':
    main()
