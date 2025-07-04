# Jarvis Tools Package
##from .sheets_tools import read_sheet, write_sheet
from .sheets_tools import read_sheet, write_sheet


"""
Calendar tools for Google Calendar integration.
"""

from .calendar_utils import get_current_time
from .create_event import create_event
from .delete_event import delete_event
from .edit_event import edit_event
from .list_events import list_events

__all__ = [
    "create_event",
    "delete_event",
    "edit_event",
    "list_events",
    "get_current_time",
]


def sheets_read_tool(params):
    # params debería ser dict con 'sheet_id' y 'range_name'
    sheet_id = params.get("sheet_id")
    range_name = params.get("range_name")
    if not sheet_id or not range_name:
        return "Error: 'sheet_id' y 'range_name' son obligatorios"
    data = read_sheet(sheet_id, range_name)
    # Formatea la salida para que sea legible en texto plano
    if not data:
        return "No hay datos en el rango especificado."
    return "\n".join([", ".join(row) for row in data])

def sheets_write_tool(params):
    sheet_id = params.get("sheet_id")
    range_name = params.get("range_name")
    values = params.get("values")  # espera lista de listas
    if not sheet_id or not range_name or not values:
        return "Error: 'sheet_id', 'range_name' y 'values' son obligatorios"
    result = write_sheet(sheet_id, range_name, values)
    return result
