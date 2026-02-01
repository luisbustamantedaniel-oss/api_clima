"""
=============================================================================
SERVICIO DE CLIMA (CAPA DE LÓGICA DE NEGOCIO)
=============================================================================

Este módulo contiene la clase WeatherService que implementa la lógica de
negocio para obtener información meteorológica.

En una arquitectura de capas (Layered Architecture), este servicio actúa
como intermediario entre:
- Controladores (reciben las peticiones HTTP)
- Clientes (se comunican con APIs externas)
- DTOs (definen la estructura de los datos de respuesta)

Responsabilidades de este servicio:
1. Validar la entrada del usuario
2. Coordinar las llamadas al cliente de OpenWeather
3. Transformar los datos crudos de la API en DTOs estructurados
4. Manejar errores de configuración

Autor: [Tu nombre]
Fecha: Enero 2026
=============================================================================
"""

# httpx es la librería para peticiones HTTP asíncronas
# La usamos para tipar el parámetro http_client
import httpx

# HTTPException permite lanzar errores HTTP que FastAPI convierte en respuestas
from fastapi import HTTPException

# Importamos el cliente que se comunica con la API de OpenWeather
# Este cliente encapsula toda la lógica de HTTP
from clients.weatherClient import OpenWeatherClient

# Importamos el DTO (Data Transfer Object) que define la estructura de respuesta
# Usar DTOs garantiza que siempre devolvamos datos con el formato correcto
from DTOs.weatherDtos import WeatherResponseDTO

# Importamos la configuración centralizada de la aplicación
from appsettings import AppSettings


class WeatherService:
    """
    Servicio principal para obtener información meteorológica.
    
    Esta clase implementa el patrón de diseño "Service Layer", que separa
    la lógica de negocio de los controladores y los clientes HTTP.
    
    Ventajas de usar un servicio:
    - Los controladores quedan simples (solo reciben y responden)
    - La lógica de negocio es reutilizable
    - Facilita el testing unitario
    - Permite agregar validaciones, caché, logging, etc.
    
    Atributos:
        client (OpenWeatherClient): Instancia del cliente HTTP para OpenWeather
    
    Ejemplo de uso:
        async with httpx.AsyncClient() as http_client:
            service = WeatherService()
            weather = await service.get_weather("Bogota", http_client)
            print(weather.temperature)
    """

    def __init__(self):
        """
        Constructor del servicio.
        
        Inicializa el servicio verificando que la configuración sea correcta
        y creando una instancia del cliente de OpenWeather.
        
        Raises:
            HTTPException(500): Si la API key de OpenWeather no está configurada.
                               Esto indica un error de configuración del servidor.
        """
        # Validación crítica: verificamos que la API key esté configurada
        # Sin la API key, no podemos hacer ninguna petición a OpenWeather
        if not AppSettings.OPENWEATHER_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="OPENWEATHER_API_KEY no está configurado. "
                       "Por favor, configura esta variable en el archivo .env"
            )
        
        # Creamos una instancia del cliente de OpenWeather
        # Este cliente se reutilizará en todas las llamadas del servicio
        self.client = OpenWeatherClient()

    async def get_weather(self, city: str, http_client: httpx.AsyncClient) -> WeatherResponseDTO:
        """
        Obtiene el clima actual de una ciudad y lo devuelve en formato estructurado.
        
        Este método coordina todo el flujo para obtener el clima:
        1. Limpia y valida el nombre de la ciudad
        2. Obtiene las coordenadas de la ciudad (Geocoding API)
        3. Obtiene los datos del clima (Weather API)
        4. Transforma los datos en un DTO estructurado
        
        Args:
            city (str): Nombre de la ciudad a consultar.
                        Puede contener espacios al inicio/final (serán eliminados).
                        Ejemplos: "Bogota", "Buenos Aires", "New York"
            
            http_client (httpx.AsyncClient): Cliente HTTP asíncrono.
                        Se inyecta desde el controlador para:
                        - Reutilizar conexiones (mejor rendimiento)
                        - Facilitar el testing con mocks
                        - Controlar el ciclo de vida de las conexiones
        
        Returns:
            WeatherResponseDTO: Objeto estructurado con:
                - city (str): Nombre de la ciudad
                - temperature (float): Temperatura en grados Celsius
                - humidity (int): Porcentaje de humedad (0-100)
                - description (str): Descripción del clima en español
        
        Raises:
            HTTPException(404): Si la ciudad no fue encontrada
            HTTPException(500): Si hay un error con la API de OpenWeather
        
        Ejemplo de respuesta:
            WeatherResponseDTO(
                city="Bogota",
                temperature=18.5,
                humidity=72,
                description="nubes dispersas"
            )
        """
        # =====================================================================
        # PASO 1: LIMPIAR Y VALIDAR LA ENTRADA
        # =====================================================================
        # Eliminamos espacios en blanco al inicio y al final del nombre
        # Esto evita errores si el usuario escribe " Bogota " en lugar de "Bogota"
        city = city.strip()

        # =====================================================================
        # PASO 2: OBTENER COORDENADAS DE LA CIUDAD
        # =====================================================================
        # La API de OpenWeather requiere latitud y longitud, no el nombre
        # Usamos la Geocoding API para convertir "Bogota" -> (4.6097, -74.0817)
        lat, lon = await self.client.get_coordinates(city, http_client)

        # =====================================================================
        # PASO 3: OBTENER DATOS DEL CLIMA
        # =====================================================================
        # Con las coordenadas, consultamos la Weather API para obtener
        # temperatura, humedad, descripción, etc.
        weather_data = await self.client.get_weather(lat, lon, http_client)

        # =====================================================================
        # PASO 4: TRANSFORMAR DATOS EN DTO
        # =====================================================================
        # La API devuelve MUCHOS datos (viento, presión, visibilidad, etc.)
        # Nosotros solo extraemos los campos que necesitamos y los
        # empaquetamos en un DTO con una estructura limpia y documentada
        #
        # Estructura de weather_data:
        # {
        #     "main": {
        #         "temp": 18.5,      <- Temperatura (la extraemos)
        #         "humidity": 72,    <- Humedad (la extraemos)
        #         "pressure": 1015,
        #         ...
        #     },
        #     "weather": [
        #         {
        #             "description": "nubes dispersas",  <- Descripción (la extraemos)
        #             "icon": "03d",
        #             ...
        #         }
        #     ],
        #     "wind": {...},
        #     "clouds": {...},
        #     ...
        # }
        
        return WeatherResponseDTO(
            city=city,                                          # Nombre de la ciudad (limpio)
            temperature=weather_data["main"]["temp"],           # Temperatura en Celsius
            humidity=weather_data["main"]["humidity"],          # Humedad en porcentaje
            description=weather_data["weather"][0]["description"]  # Descripción en español
        )
