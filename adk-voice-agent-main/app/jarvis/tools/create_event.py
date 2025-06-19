"""
Create event tool for Google Calendar integration.
"""

import traceback
from .calendar_utils import get_calendar_service, parse_datetime


def create_event(
    summary: str,
    start_time: str,
    end_time: str,
) -> dict:
    """
    Create a new event in Google Calendar.

    Args:
        summary (str): Event title/summary
        start_time (str): Start time (e.g., "2025-06-17 05:00")
        end_time (str): End time (e.g., "2025-06-17 06:00")

    Returns:
        dict: Information about the created event or error details
    """
    try:
        # Obtener servicio de Google Calendar
        service = get_calendar_service()
        if not service:
            return {
                "status": "error",
                "message": "❌ No se pudo autenticar con Google Calendar. Verifica las credenciales.",
            }

        calendar_id = "primary"

        # Parsear fechas
        start_dt = parse_datetime(start_time)
        end_dt = parse_datetime(end_time)

        if not start_dt or not end_dt:
            print(f"❌ Error al parsear fechas. start_dt={start_dt}, end_dt={end_dt}")
            return {
                "status": "error",
                "message": "❌ Formato de fecha/hora inválido. Usa 'YYYY-MM-DD HH:MM'.",
            }

        if end_dt <= start_dt:
            print(f"❌ Error: hora final {end_dt} es menor o igual a la hora inicial {start_dt}")
            return {
                "status": "error",
                "message": "❌ La hora de finalización debe ser posterior a la hora de inicio.",
            }

        # Obtener zona horaria desde las configuraciones del calendario
        timezone_id = "America/Managua"  # Default
        try:
            settings = service.settings().list().execute()
            for setting in settings.get("items", []):
                if setting.get("id") == "timezone":
                    timezone_id = setting.get("value")
                    break
        except Exception as tz_err:
            print("⚠️ No se pudo obtener la zona horaria. Se usará la predeterminada:", timezone_id)

        # Construir evento
        event_body = {
            "summary": summary,
            "start": {
                "dateTime": start_dt.isoformat(),
                "timeZone": timezone_id,
            },
            "end": {
                "dateTime": end_dt.isoformat(),
                "timeZone": timezone_id,
            },
        }

        # Crear evento
        event = service.events().insert(calendarId=calendar_id, body=event_body).execute()

        print("✅ Evento creado:", event.get("htmlLink"))
        return {
            "status": "success",
            "message": "✅ Evento creado exitosamente.",
            "event_id": event.get("id"),
            "event_link": event.get("htmlLink", ""),
        }

    except Exception as e:
        print("❌ Excepción al crear el evento:")
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"❌ Error al crear el evento: {str(e)}",
            "trace": traceback.format_exc()
        }
