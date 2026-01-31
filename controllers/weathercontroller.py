"""
=============================================================================
CONTROLADOR DE CLIMA (CAPA DE PRESENTACIÓN)
=============================================================================

Este módulo contiene el controlador (router) que maneja las peticiones HTTP
relacionadas con el clima.

En la arquitectura MVC (Model-View-Controller) o en arquitecturas de capas,
el controlador es responsable de:

1. RECIBIR las peticiones HTTP del cliente
2. EXTRAER los parámetros de la petición (path, query, body)
3. DELEGAR la lógica de negocio al servicio correspondiente
4. DEVOLVER la respuesta al cliente en el formato correcto

¿Por qué el controlador no debe tener lógica de negocio?
--------------------------------------------------------
- Mantiene el código organizado y fácil de mantener
- Permite reutilizar la lógica en otros controladores o servicios
- Facilita el testing (puedes probar el servicio sin HTTP)
- Sigue el principio de responsabilidad única (SRP)

Rutas disponibles:
- GET /api/weather/{city} - Obtiene el clima de una ciudad

Autor: [Tu nombre]
Fecha: Enero 2026
=============================================================================
"""

# httpx es la librería para peticiones HTTP asíncronas
# AsyncClient permite reutilizar conexiones de forma eficiente
import httpx

# APIRouter permite agrupar rutas relacionadas en un módulo separado
# Es como un "mini-app" que luego se incluye en la aplicación principal
from fastapi import APIRouter

# Importamos el servicio que contiene la lógica de negocio
# El controlador NUNCA debe acceder directamente al cliente HTTP o APIs externas
from services.weatherservices import WeatherService

# Importamos el DTO para tipar la respuesta
# Esto permite que FastAPI genere documentación automática
from DTOs.weatherDtos import WeatherResponseDTO


# =============================================================================
# CONFIGURACIÓN DEL ROUTER
# =============================================================================
# Creamos un router con el prefijo "/api"
# Todas las rutas definidas aquí comenzarán con /api
# Ejemplo: @router.get("/weather/{city}") -> GET /api/weather/{city}
router = APIRouter(
    prefix="/api",  # Prefijo para todas las rutas de este router
    tags=["Weather"]  # Etiqueta para agrupar en la documentación Swagger
)


# =============================================================================
# ENDPOINT: OBTENER CLIMA DE UNA CIUDAD
# =============================================================================
@router.get(
    "/weather/{city}",  # Ruta con parámetro de path {city}
    response_model=WeatherResponseDTO,  # Define el esquema de respuesta
    summary="Obtener clima actual",  # Título en Swagger
    description="Obtiene la información meteorológica actual de una ciudad específica",
    responses={
        200: {
            "description": "Clima obtenido exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "city": "Bogota",
                        "temperature": 18.5,
                        "humidity": 72,
                        "description": "nubes dispersas"
                    }
                }
            }
        },
        404: {
            "description": "Ciudad no encontrada",
            "content": {
                "application/json": {
                    "example": {"detail": "Ciudad 'xyz' no encontrada"}
                }
            }
        },
        500: {
            "description": "Error del servidor o API key no configurada",
            "content": {
                "application/json": {
                    "example": {"detail": "OPENWEATHER_API_KEY no está configurado"}
                }
            }
        }
    }
)
async def get_weather(city: str) -> WeatherResponseDTO:
    """
    Obtiene el clima actual de una ciudad.
    
    Este endpoint recibe el nombre de una ciudad y devuelve información
    meteorológica incluyendo temperatura, humedad y descripción del clima.
    
    Args:
        city (str): Nombre de la ciudad a consultar.
                   Se extrae automáticamente de la URL.
                   Ejemplos: "Bogota", "Madrid", "New York"
    
    Returns:
        WeatherResponseDTO: Objeto JSON con:
            - city: Nombre de la ciudad
            - temperature: Temperatura en Celsius
            - humidity: Porcentaje de humedad
            - description: Descripción del clima en español
    
    Raises:
        HTTPException(404): Si la ciudad no existe
        HTTPException(500): Si hay problemas con la API de OpenWeather
    
    Ejemplo de uso:
        GET /api/weather/Bogota
        
        Respuesta:
        {
            "city": "Bogota",
            "temperature": 18.5,
            "humidity": 72,
            "description": "nubes dispersas"
        }
    """
    # =========================================================================
    # CREAMOS EL CLIENTE HTTP ASÍNCRONO
    # =========================================================================
    # Usamos 'async with' para manejar automáticamente el ciclo de vida
    # del cliente HTTP. Esto garantiza que:
    # 1. Las conexiones se reutilicen eficientemente
    # 2. Los recursos se liberen al finalizar
    # 3. No haya fugas de memoria o conexiones abiertas
    async with httpx.AsyncClient() as http_client:
        
        # =====================================================================
        # DELEGAMOS LA LÓGICA AL SERVICIO
        # =====================================================================
        # El controlador NO debe contener lógica de negocio
        # Solo crea las dependencias necesarias y llama al servicio
        weather_service = WeatherService()
        
        # Llamamos al método del servicio y esperamos la respuesta
        # 'await' es necesario porque es una operación asíncrona
        weather_response = await weather_service.get_weather(city, http_client)
        
        # Devolvemos la respuesta
        # FastAPI automáticamente:
        # 1. Valida que cumpla el esquema WeatherResponseDTO
        # 2. Serializa el objeto a JSON
        # 3. Establece el Content-Type: application/json
        # 4. Devuelve un código 200 OK
        return weather_response