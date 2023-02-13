# -*- coding: utf-8 -*-

# Sample Python code for youtube.subscriptions.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
import pprint

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "Téléchargements/code_secret_client_1018176271212-50i7knmbk94vgorr97om0ng48kc4i03k.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.subscriptions().list(
        part="snippet,contentDetails",
        channelId="UC8SPevb2kwoaqu8VyAF1L6g",
        maxResults=50
    )
    response = request.execute()


    subscriptions = response["items"]
    while 'nextPageToken' in response:
        request = youtube.subscriptions().list(
            part="snippet,contentDetails",
            channelId="UC8SPevb2kwoaqu8VyAF1L6g",
            maxResults=50,
            pageToken=response['nextPageToken'])
        response = request.execute()
        subscriptions += response["items"]



    with open("sample.json", "w") as outfile:
        json.dump(subscriptions,outfile,indent=4)
    
    return subscriptions



if __name__ == "__main__":
    main()
