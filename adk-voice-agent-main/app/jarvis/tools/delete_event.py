"""
Delete event tool for Google Calendar integration.
"""

from .calendar_utils import get_calendar_service
from session_store import session_tokens

def delete_event(
    session_id: str,
    event_id: str,
    confirm: bool,
) -> dict:
    """
    Delete an event from Google Calendar.

    Args:
        event_id (str): The unique ID of the event to delete
        confirm (bool): Confirmation flag (must be set to True to delete)

    Returns:
        dict: Operation status and details
    """
    # Safety check - require explicit confirmation
    if not confirm:
        return {
            "status": "error",
            "message": "Please confirm deletion by setting confirm=True",
        }

    try:

        # Obtén los tokens de la sesión
        tokens = session_tokens.get(session_id)
        if not tokens:
            return {
                "status": "error",
                "message": "No se encontraron credenciales para esta sesión.",
                "events": [],
            }
            
        # Get calendar service
        service = get_calendar_service(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            client_id=tokens["client_id"],
            client_secret=tokens["client_secret"],  
        )
        if not service:
            return {
                "status": "error",
                "message": "Failed to authenticate with Google Calendar. Please check credentials.",
            }

        # Always use primary calendar
        calendar_id = "primary"

        # Call the Calendar API to delete the event
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()

        return {
            "status": "success",
            "message": f"Event {event_id} has been deleted successfully",
            "event_id": event_id,
        }

    except Exception as e:
        return {"status": "error", "message": f"Error deleting event: {str(e)}"}
