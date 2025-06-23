from typing import List
import os
import json

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


# Ruta al token de autenticación
# TOKEN_PATH = os.path.expanduser("/credentials.json")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/calendar"
]

# Servicio de Google Sheets
# def get_sheets_service():
#     with open(TOKEN_PATH, "r") as f:
#         creds_data = json.load(f)

#     creds = Credentials.from_authorized_user_info(
#         creds_data,
#         scopes=[
#             "https://www.googleapis.com/auth/spreadsheets",
#             "https://www.googleapis.com/auth/calendar"
#         ]
#     )

#     if creds.expired and creds.refresh_token:
#         from google.auth.transport.requests import Request
#         creds.refresh(Request())
#         with open(TOKEN_PATH, "w") as token_file:
#             token_file.write(creds.to_json())

#     return build("sheets", "v4", credentials=creds)

def get_sheets_service(access_token, refresh_token=None, client_id=None, client_secret=None):
    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES,
    )
    return build("sheets", "v4", credentials=creds)
    
# Funciones básicas sin decoradores
# def sheets_read_tool(sheet_id: str, range_name: str) -> str:
#     """Lee valores de un rango específico en una hoja de cálculo de Google Sheets."""
#     if not sheet_id or not range_name:
#         return "Error: 'sheet_id' y 'range_name' son obligatorios"

#     try:
#         service = get_sheets_service()
#         result = service.spreadsheets().values().get(
#             spreadsheetId=sheet_id,
#             range=range_name
#         ).execute()
#         values = result.get("values", [])

#         if not values:
#             return "No hay datos en el rango especificado."

#         return "\n".join([", ".join(row) for row in values])
    
#     except Exception as e:
#         return f"Error al leer la hoja: {str(e)}"

def sheets_read_tool(sheet_id: str, range_name: str, access_token, refresh_token=None, client_id=None, client_secret=None) -> str:
    if not sheet_id or not range_name:
        return "Error: 'sheet_id' y 'range_name' son obligatorios"

    try:
        service = get_sheets_service(access_token, refresh_token, client_id, client_secret)
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=range_name
        ).execute()
        values = result.get("values", [])

        if not values:
            return "No hay datos en el rango especificado."

        return "\n".join([", ".join(row) for row in values])
    
    except Exception as e:
        return f"Error al leer la hoja: {str(e)}"


# def sheets_write_tool(sheet_id: str, range_name: str, values: List[List[str]]) -> str:
#     """Escribe valores en un rango específico de una hoja de Google Sheets."""
#     if not sheet_id or not range_name or not values:
#         return "Error: 'sheet_id', 'range_name' y 'values' son obligatorios"

#     try:
#         service = get_sheets_service()
#         body = {"values": values}

#         result = service.spreadsheets().values().update(
#             spreadsheetId=sheet_id,
#             range=range_name,
#             valueInputOption="RAW",
#             body=body
#         ).execute()

#         return f"Se escribieron {result.get('updatedCells')} celdas."
    
#     except Exception as e:
#         return f"Error al escribir en la hoja: {str(e)}"

def sheets_write_tool(sheet_id: str, range_name: str, values: List[List[str]], access_token=None, refresh_token=None, client_id=None, client_secret=None) -> str:
    if not sheet_id or not range_name or not values:
        return "Error: 'sheet_id', 'range_name' y 'values' son obligatorios"

    try:
        service = get_sheets_service(access_token, refresh_token, client_id, client_secret)
        body = {"values": values}

        result = service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()

        return f"Se escribieron {result.get('updatedCells')} celdas."
    
    except Exception as e:
        return f"Error al escribir en la hoja: {str(e)}"


# def sheets_append_tool(sheet_id: str, range_name: str, values: List[List[str]]) -> str:
#     """Agrega nuevas filas al final de una hoja de Google Sheets."""
#     if not sheet_id or not range_name or not values:
#         return "Error: 'sheet_id', 'range_name' y 'values' son obligatorios"

#     try:
#         service = get_sheets_service()
#         body = {"values": values}

#         result = service.spreadsheets().values().append(
#             spreadsheetId=sheet_id,
#             range=range_name,
#             valueInputOption="RAW",
#             insertDataOption="INSERT_ROWS",
#             body=body
#         ).execute()

#         return f"Se agregaron {len(values)} filas nuevas."
    
#     except Exception as e:
#         return f"Error al agregar filas: {str(e)}"

def sheets_append_tool(sheet_id: str, range_name: str, values: List[List[str]], access_token=None, refresh_token=None, client_id=None, client_secret=None) -> str:
    if not sheet_id or not range_name or not values:
        return "Error: 'sheet_id', 'range_name' y 'values' son obligatorios"

    try:
        service = get_sheets_service(access_token, refresh_token, client_id, client_secret)
        body = {"values": values}

        result = service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range=range_name,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()

        return f"Se agregaron {len(values)} filas nuevas."
    
    except Exception as e:
        return f"Error al agregar filas: {str(e)}"


# def find_and_update_task(sheet_id: str, task_name: str, new_status: str, search_range: str = "Tareas!A:E") -> str:
#     """Busca una tarea por nombre y actualiza su estado."""
#     if not all([sheet_id, task_name, new_status]):
#         return "Error: sheet_id, task_name y new_status son obligatorios"

#     try:
#         service = get_sheets_service()
        
#         # Leer todas las tareas
#         result = service.spreadsheets().values().get(
#             spreadsheetId=sheet_id,
#             range=search_range
#         ).execute()
#         values = result.get("values", [])

#         if not values:
#             return "No se encontraron tareas en la hoja."

#         # Buscar la tarea (asumiendo que el nombre está en la columna A)
#         for i, row in enumerate(values):
#             if len(row) > 0 and row[0].lower() == task_name.lower():
#                 # Actualizar el estado (asumiendo que está en la columna E, índice 4)
#                 sheet_name = search_range.split('!')[0]
#                 update_range = f"{sheet_name}!E{i + 1}"
#                 body = {"values": [[new_status]]}
                
#                 service.spreadsheets().values().update(
#                     spreadsheetId=sheet_id,
#                     range=update_range,
#                     valueInputOption="RAW",
#                     body=body
#                 ).execute()
                
#                 return f"Tarea '{task_name}' actualizada a '{new_status}'"

#         return f"No se encontró la tarea '{task_name}'"
    
#     except Exception as e:
#         return f"Error al actualizar la tarea: {str(e)}"

def find_and_update_task(sheet_id: str, task_name: str, new_status: str, access_token=None, refresh_token=None, client_id=None, client_secret=None, search_range: str = "Tareas!A:E") -> str:
    if not all([sheet_id, task_name, new_status]):
        return "Error: sheet_id, task_name y new_status son obligatorios"

    try:
        service = get_sheets_service(access_token, refresh_token, client_id, client_secret)
        
        # Leer todas las tareas
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=search_range
        ).execute()
        values = result.get("values", [])

        if not values:
            return "No se encontraron tareas en la hoja."

        # Buscar la tarea (asumiendo que el nombre está en la columna A)
        for i, row in enumerate(values):
            if len(row) > 0 and row[0].lower() == task_name.lower():
                # Actualizar el estado (asumiendo que está en la columna E, índice 4)
                sheet_name = search_range.split('!')[0]
                update_range = f"{sheet_name}!E{i + 1}"
                body = {"values": [[new_status]]}
                
                service.spreadsheets().values().update(
                    spreadsheetId=sheet_id,
                    range=update_range,
                    valueInputOption="RAW",
                    body=body
                ).execute()
                
                return f"Tarea '{task_name}' actualizada a '{new_status}'"

        return f"No se encontró la tarea '{task_name}'"
    
    except Exception as e:
        return f"Error al actualizar la tarea: {str(e)}"


# Funciones de conveniencia
# def add_task_to_sheet(sheet_id: str, task_title: str, description: str = "", due_date: str = "", priority: str = "Media"):
#     """Agrega una nueva tarea a la hoja de tareas."""
#     import datetime
    
#     values = [[
#         task_title,
#         description,
#         due_date,
#         priority,
#         "Pendiente",
#         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     ]]
    
#     return sheets_append_tool(sheet_id, "Tareas!A:F", values)



# def get_pending_tasks(sheet_id: str):
#     """Obtiene todas las tareas pendientes."""
#     return sheets_read_tool(sheet_id, "Tareas!A:F")

def add_task_to_sheet(sheet_id: str, task_title: str, description: str = "", due_date: str = "", priority: str = "Media", access_token=None, refresh_token=None, client_id=None, client_secret=None):
    import datetime
    values = [[
        task_title,
        description,
        due_date,
        priority,
        "Pendiente",
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]]
    return sheets_append_tool(sheet_id, "Tareas!A:F", values, access_token, refresh_token, client_id, client_secret)

def get_pending_tasks(sheet_id: str, access_token=None, refresh_token=None, client_id=None, client_secret=None):
    return sheets_read_tool(sheet_id, "Tareas!A:F", access_token, refresh_token, client_id, client_secret)


# Asignaciones útiles
read_sheet = sheets_read_tool
write_sheet = sheets_write_tool
append_sheet = sheets_append_tool
update_task = find_and_update_task
add_task = add_task_to_sheet
get_tasks = get_pending_tasks