"""
=============================================================================
CLIENTE HTTP PARA LA API DE OPENWEATHER
=============================================================================

Este módulo contiene la clase OpenWeatherClient que se encarga de realizar
las peticiones HTTP a la API externa de OpenWeatherMap.

La API de OpenWeather requiere dos llamadas separadas:
1. Geocoding API: Convierte el nombre de la ciudad en coordenadas (lat, lon)
2. Weather API: Obtiene los datos meteorológicos usando las coordenadas

Documentación oficial de OpenWeather:
- Geocoding: https://openweathermap.org/api/geocoding-api
- Weather: https://openweathermap.org/current

Autor: [Tu nombre]
Fecha: Enero 2026
=============================================================================
"""

# httpx es una librería moderna para hacer peticiones HTTP asíncronas en Python
# Es similar a 'requests' pero soporta async/await de forma nativa
import httpx

# HTTPException nos permite lanzar errores HTTP con códigos de estado específicos
# FastAPI los convierte automáticamente en respuestas HTTP apropiadas
from fastapi import HTTPException

# Importamos la configuración centralizada de la aplicación
# Contiene las URLs de la API, la API key y otros parámetros
from appsettings import AppSettings


class OpenWeatherClient:
    """
    Cliente HTTP para interactuar con la API de OpenWeatherMap.
    
    Esta clase encapsula toda la lógica de comunicación con la API externa,
    siguiendo el patrón de diseño "Client" o "Gateway". Esto permite:
    
    - Separar la lógica de HTTP de la lógica de negocio
    - Facilitar el testing mediante mocks
    - Centralizar el manejo de errores de la API externa
    - Reutilizar el cliente en diferentes servicios si es necesario
    
    Ejemplo de uso:
        async with httpx.AsyncClient() as http_client:
            weather_client = OpenWeatherClient()
            lat, lon = await weather_client.get_coordinates("Bogota", http_client)
            weather = await weather_client.get_weather(lat, lon, http_client)
    """

    def __init__(self):
        """
        Constructor de la clase.
        
        Actualmente no requiere inicialización especial, pero se mantiene
        por si en el futuro se necesita inyectar dependencias o configuración.
        """
        pass

    async def get_coordinates(self, city: str, http_client: httpx.AsyncClient) -> tuple[float, float]:
        """
        Obtiene las coordenadas geográficas (latitud y longitud) de una ciudad.
        
        La API de OpenWeather requiere coordenadas para obtener el clima,
        por lo que primero debemos convertir el nombre de la ciudad a coordenadas
        usando la Geocoding API.
        
        Args:
            city (str): Nombre de la ciudad a buscar (ej: "Bogota", "Madrid")
            http_client (httpx.AsyncClient): Cliente HTTP asíncrono compartido.
                                             Se pasa como parámetro para reutilizar
                                             conexiones y mejorar el rendimiento.
        
        Returns:
            tuple[float, float]: Tupla con (latitud, longitud) de la ciudad
        
        Raises:
            HTTPException(404): Si la ciudad no fue encontrada
            HTTPException(status_code): Si hay un error en la API de OpenWeather
        
        Ejemplo:
            lat, lon = await client.get_coordinates("Bogota", http_client)
            # lat = 4.6097, lon = -74.0817
        """
        # Realizamos la petición GET a la API de Geocoding de OpenWeather
        # Usamos 'await' porque es una operación asíncrona (I/O bound)
        response = await http_client.get(
            AppSettings.GEOCODING_URL,  # URL base de la API de geocoding
            params={
                "q": city,                              # Nombre de la ciudad a buscar
                "limit": 1,                             # Solo queremos el primer resultado
                "appid": AppSettings.OPENWEATHER_API_KEY  # API key para autenticación
            },
            timeout=AppSettings.TIMEOUT_SECONDS  # Tiempo máximo de espera (evita bloqueos)
        )

        # Verificamos si la respuesta fue exitosa (código 200)
        # Si no lo fue, lanzamos una excepción con el código de error
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error al obtener coordenadas desde la API de OpenWeather"
            )

        # Convertimos la respuesta JSON a un diccionario de Python
        data = response.json()

        # La API devuelve una lista vacía si no encuentra la ciudad
        # En ese caso, informamos al usuario con un error 404
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"Ciudad '{city}' no encontrada. Verifica el nombre e intenta de nuevo."
            )

        # Extraemos las coordenadas del primer resultado
        # La API devuelve una lista de coincidencias, tomamos la primera
        lat = data[0]["lat"]  # Latitud (ej: 4.6097 para Bogotá)
        lon = data[0]["lon"]  # Longitud (ej: -74.0817 para Bogotá)

        return lat, lon

    async def get_weather(self, lat: float, lon: float, http_client: httpx.AsyncClient) -> dict:
        """
        Obtiene los datos meteorológicos actuales para unas coordenadas específicas.
        
        Esta función consulta la Current Weather API de OpenWeather para obtener
        información como temperatura, humedad, descripción del clima, etc.
        
        Args:
            lat (float): Latitud de la ubicación (ej: 4.6097)
            lon (float): Longitud de la ubicación (ej: -74.0817)
            http_client (httpx.AsyncClient): Cliente HTTP asíncrono compartido
        
        Returns:
            dict: Diccionario con todos los datos meteorológicos de la API.
                  Estructura principal:
                  {
                      "main": {"temp": 20.5, "humidity": 80, ...},
                      "weather": [{"description": "cielo claro", ...}],
                      "wind": {"speed": 3.5, ...},
                      ...
                  }
        
        Raises:
            HTTPException(status_code): Si hay un error en la API de OpenWeather
        
        Ejemplo:
            weather = await client.get_weather(4.6097, -74.0817, http_client)
            print(weather["main"]["temp"])  # Imprime la temperatura
        """
        # Realizamos la petición GET a la API de Weather de OpenWeather
        response = await http_client.get(
            AppSettings.WEATHER_URL,  # URL base de la API de clima
            params={
                "lat": lat,                             # Latitud obtenida previamente
                "lon": lon,                             # Longitud obtenida previamente
                "appid": AppSettings.OPENWEATHER_API_KEY,  # API key para autenticación
                "units": AppSettings.UNITS,             # "metric" para Celsius, "imperial" para Fahrenheit
                "lang": AppSettings.LANGUAGE            # "es" para descripciones en español
            },
            timeout=AppSettings.TIMEOUT_SECONDS  # Tiempo máximo de espera
        )

        # Verificamos si la respuesta fue exitosa
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error al obtener datos meteorológicos desde la API de OpenWeather"
            )

        # Devolvemos el JSON completo con todos los datos del clima
        # El servicio se encargará de extraer solo los campos necesarios
        return response.json()