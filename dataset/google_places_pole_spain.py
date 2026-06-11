import requests
import pandas as pd
import time
from datetime import datetime

API_KEY = "TU_API_KEY"

provinces = [
    "Madrid",
    "Barcelona",
    "Valencia",
    "Sevilla",
    "Málaga",
    "Murcia",
    "Alicante",
    "Zaragoza",
    "Bilbao",
    "Valladolid",
    "A Coruña",
    "Vigo",
    "Oviedo",
    "Santander",
    "Pamplona",
    "Logroño",
    "Salamanca",
    "León",
    "Burgos",
    "Toledo",
    "Guadalajara",
    "Cuenca",
    "Albacete",
    "Castellón",
    "Tarragona",
    "Lleida",
    "Girona",
    "Granada",
    "Almería",
    "Córdoba",
    "Jaén",
    "Cádiz",
    "Huelva",
    "Badajoz",
    "Cáceres",
    "Ourense",
    "Lugo",
    "Palencia",
    "Segovia",
    "Soria",
    "Zamora",
    "Ávila",
    "Huesca",
    "Teruel",
    "Las Palmas",
    "Santa Cruz de Tenerife",
    "Ceuta",
    "Melilla"
]

queries = [
    "pole dance",
    "pole dance studio",
    "pole fitness",
    "pole studio",
    "pole academy",
    "pole art",
    "pole school",
    "pole classes",
    "pole training",
    "aerial pole",
    "aerial dance",
    "pole and aerial",
    "exotic pole",
    "pole sport",
    "pole fitness studio"
]

rows = []

for province in provinces:

    print(f"\nBuscando en {province}")

    for query in queries:

        search_query = f"{query} {province} Spain"

        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

        params = {
            "query": search_query,
            "key": API_KEY
        }

        while True:

            response = requests.get(
                url,
                params=params,
                timeout=30
            )

            data = response.json()

            for place in data.get("results", []):

                rows.append({

                    # Datos de búsqueda
                    "search_query": query,
                    "province_search": province,
                    "timestamp": datetime.now(),

                    # Identificación
                    "place_id": place.get("place_id"),
                    "name": place.get("name"),

                    # Dirección
                    "formatted_address":
                        place.get("formatted_address"),

                    # Valoraciones
                    "rating":
                        place.get("rating"),

                    "user_ratings_total":
                        place.get("user_ratings_total"),

                    # Coordenadas
                    "lat":
                        place.get("geometry", {})
                             .get("location", {})
                             .get("lat"),

                    "lng":
                        place.get("geometry", {})
                             .get("location", {})
                             .get("lng"),

                    # Estado
                    "business_status":
                        place.get("business_status"),

                    # Categorías
                    "types":
                        ", ".join(place.get("types", []))

                })

            next_page_token = data.get(
                "next_page_token"
            )

            if not next_page_token:
                break

            time.sleep(2)

            params = {
                "pagetoken": next_page_token,
                "key": API_KEY
            }

        time.sleep(0.2)

df = pd.DataFrame(rows)

# NO eliminar duplicados
# NO eliminar nulos

df.to_csv(
    "pole_dance_spain_raw.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nDataset generado")
print(f"Filas: {len(df)}")
print(f"Columnas: {len(df.columns)}")

print("\nPrimeras filas:")
print(df.head())