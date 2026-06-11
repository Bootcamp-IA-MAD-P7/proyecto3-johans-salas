import os
import pandas as pd
import requests
import time
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Recupera la API Key de forma segura
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

RAW_CSV_PATH = "pole_dance_spain_raw.csv"
OUTPUT_CSV_PATH = "pole_dance_spain_enriched.csv"

# Valida que la clave se ha cargado correctamente antes de iniciar
if not API_KEY:
    print("Error: No se encontró la variable GOOGLE_PLACES_API_KEY en el archivo .env")
    exit()

def obtener_detalles_place(place_id, api_key):
    if pd.isna(place_id) or not place_id:
        return {}
        
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    fields = "website,formatted_phone_number,opening_hours,url,geometry"
    
    params = {
        "place_id": place_id,
        "fields": fields,
        "key": api_key,
        "language": "es"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                result = data.get("result", {})
                
                # Estructura los horarios en una sola cadena de texto
                horarios = result.get("opening_hours", {}).get("weekday_text", [])
                horarios_str = " | ".join(horarios) if horarios else None
                
                return {
                    "website": result.get("website"),
                    "phone": result.get("formatted_phone_number"),
                    "horario": horarios_str,
                    "google_maps_url": result.get("url"),
                    "lat_precisa": result.get("geometry", {}).get("location", {}).get("lat"),
                    "lng_precisa": result.get("geometry", {}).get("location", {}).get("lng")
                }
    except Exception as e:
        print(f"\nError de conexión con el place_id {place_id}: {e}")
        
    return {}

print("Leyendo el dataset raw...")
try:
    df_raw = pd.read_csv(RAW_CSV_PATH, encoding="utf-8-sig")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo {RAW_CSV_PATH}. Ejecuta primero el script google_places_pole_spain.py.")
    exit()

total_filas = len(df_raw)
print(f"Se han cargado {total_filas} filas. Iniciando enriquecimiento fila por fila...")

# Se preparan las listas donde guardaremos los datos columna por columna
websites = []
phones = []
horarios = []
urls = []
lats_precisas = []
lngs_precisas = []


for index, row in df_raw.iterrows():
    place_id = row.get("place_id")
    
    # Muestra el progreso en la terminal
    if (index + 1) % 10 == 0 or (index + 1) == total_filas:
        print(f"Procesando fila {index + 1}/{total_filas}...")
        
    # Llama a la API para esta fila concreta
    detalles = obtener_detalles_place(place_id, API_KEY)
    
    # Guarda los datos correspondientes (si la API no devolvió nada, guarda None)
    websites.append(detalles.get("website"))
    phones.append(detalles.get("phone"))
    horarios.append(detalles.get("horario"))
    urls.append(detalles.get("google_maps_url"))
    lats_precisas.append(detalles.get("lat_precisa"))
    lngs_precisas.append(detalles.get("lngs_precisa"))
    
    # Pausa de cortesía obligatoria para no saturar la cuota por segundo
    time.sleep(0.1)

# Añade las nuevas columnas directamente al DataFrame original
df_raw["website"] = websites
df_raw["phone"] = phones
df_raw["horario"] = horarios
df_raw["google_maps_url"] = urls
df_raw["lat_precisa"] = lats_precisas
df_raw["lng_precisa"] = lngs_precisas

# Guarda el archivo final manteniendo la estructura idéntica del archivo original
df_raw.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8-sig")

print(f"\n¡Proceso finalizado!")
print(f"Archivo guardado en: {OUTPUT_CSV_PATH}")
print(f"Filas totales conservadas: {len(df_raw)}")