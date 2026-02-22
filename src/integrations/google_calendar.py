import logging
from datetime import datetime

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


class GoogleCalendarClient:
    def __init__(self, credentials: Credentials):
        self.service = build("calendar", "v3", credentials=credentials)

    def create_event(self, summary: str, start_dt: datetime, end_dt: datetime, description: str = "") -> str:
        event = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_dt.isoformat(), "timeZone": "UTC"},
            "end": {"dateTime": end_dt.isoformat(), "timeZone": "UTC"},
        }
        result = self.service.events().insert(calendarId="primary", body=event).execute()
        logger.info("calendar event created", extra={"event_id": result["id"]})
        return result["id"]

    def delete_event(self, event_id: str) -> None:
        self.service.events().delete(calendarId="primary", eventId=event_id).execute()
        logger.info("calendar event deleted", extra={"event_id": event_id})
