from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def youtube_upload(video_path, title, description, hash_tags: list, port=8888):
    # Set your YouTube API credentials
    client_secrets_file = "client_secrets.json"
    api_service_name = "youtube"
    api_version = "v3"
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    # Create the API client and authenticate
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_local_server(port=port, verify=False)
    youtube = build(api_service_name, api_version, credentials=credentials)

    # Create a request body with the video details
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": hash_tags,
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    # Upload the video
    media = MediaFileUpload(video_path)
    response = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media).execute()

    print("Video uploaded successfully. Video ID:", response["id"])
