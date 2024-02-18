import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import Resource

from site_parser import parse_chsu_page
from ScheduleSubject import ScheduleSubject

SCOPES = 'https://www.googleapis.com/auth/calendar'
GTM_OFF = '+03:00'


def main():
    schedule_subjects = parse_chsu_page()

    service = init_calendar_service()
    gmt_off = '+03:00'
    try:
        for subj in schedule_subjects:
            if not check_event_existing(subj, service):
                event = {
                    'summary': subj.subject_name,
                    'start': {'dateTime': f'{subj.start_time.isoformat()}{gmt_off}'},
                    'end': {'dateTime': f'{subj.end_time.isoformat()}{gmt_off}'}
                }
                service.events().insert(calendarId='primary', sendNotifications=False, body=event).execute()
                print(f"Event {subj.subject_name} {subj.start_time} - {subj.end_time} has been added to calendar")
            else:
                print(f"Event {subj.subject_name} {subj.start_time} - {subj.end_time} already exists")

    except HttpError as error:
        print(f"An error occurred: {error}")


def init_calendar_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("secrets/token.json"):
        creds = Credentials.from_authorized_user_file("secrets/token.json")
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "secrets/credentials.json",
                scopes=SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("secrets/token.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


def check_event_existing(subj: ScheduleSubject, service: Resource) -> bool:
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=subj.start_time.isoformat() + GTM_OFF,
            timeMax=subj.end_time.isoformat() + GTM_OFF,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    return len(events) > 0


if __name__ == "__main__":
    main()
