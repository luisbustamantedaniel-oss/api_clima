"""
=============================================================================
CONFIGURACIÓN CENTRALIZADA DE LA APLICACIÓN
=============================================================================

Este módulo contiene la configuración global de la aplicación, cargando
las variables de entorno desde el archivo .env y exponiendo constantes
de configuración.

¿Por qué usar un archivo de configuración centralizado?
-------------------------------------------------------
1. SEGURIDAD: Las API keys y secretos no se guardan en el código fuente
2. FLEXIBILIDAD: Puedes cambiar configuraciones sin modificar código
3. AMBIENTES: Fácil de tener diferentes configuraciones (dev, staging, prod)
4. MANTENIBILIDAD: Un solo lugar para todas las configuraciones

Contenido del archivo .env (ejemplo):
-------------------------------------
OPENWEATHER_API_KEY=tu_api_key_aquí
OPENWEATHER_GEOCODING_URL=http://api.openweathermap.org/geo/1.0/direct
OPENWEATHER_WEATHER_URL=http://api.openweathermap.org/data/2.5/weather

IMPORTANTE: El archivo .env NUNCA debe subirse a Git
Agrégalo a tu .gitignore para proteger tus credenciales

Autor: [Tu nombre]
Fecha: Enero 2026
=============================================================================
"""

# os proporciona funciones para interactuar con el sistema operativo
# Usamos os.getenv() para leer variables de entorno
import os

# python-dotenv permite cargar variables de entorno desde un archivo .env
# Esto es muy útil en desarrollo para no tener que configurar variables
# de entorno del sistema manualmente
from dotenv import load_dotenv


# =============================================================================
# CARGAR VARIABLES DE ENTORNO
# =============================================================================
# load_dotenv() busca un archivo llamado .env en el directorio actual
# y carga todas las variables definidas en él como variables de entorno
# 
# Ejemplo de contenido de .env:
# OPENWEATHER_API_KEY=abc123
# 
# Después de load_dotenv(), puedes acceder con os.getenv("OPENWEATHER_API_KEY")
load_dotenv()


class AppSettings:
    """
    Clase de configuración que contiene todas las constantes de la aplicación.
    
    Usamos una clase en lugar de variables sueltas por las siguientes razones:
    - Agrupa todas las configuraciones en un solo lugar
    - Permite validación y transformación de valores
    - Facilita el autocompletado en el IDE
    - Es más fácil de mockear en tests
    
    Uso:
        from appsettings import AppSettings
        
        api_key = AppSettings.OPENWEATHER_API_KEY
        timeout = AppSettings.TIMEOUT_SECONDS
    
    Nota: Todos los atributos son de clase (class attributes), no de instancia.
    Esto significa que no necesitas crear una instancia para usarlos:
        AppSettings.OPENWEATHER_API_KEY  # ✓ Correcto
        AppSettings().OPENWEATHER_API_KEY  # También funciona, pero innecesario
    """

    # =========================================================================
    # CONFIGURACIÓN DE LA API DE OPENWEATHER
    # =========================================================================
    
    # API Key de OpenWeather - REQUERIDA
    # Se obtiene gratis registrándose en: https://openweathermap.org/api
    # Esta key debe mantenerse PRIVADA y nunca subirse a repositorios públicos
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    
    # URL de la API de Geocoding (convertir ciudad -> coordenadas)
    # Documentación: https://openweathermap.org/api/geocoding-api
    # Ejemplo: http://api.openweathermap.org/geo/1.0/direct?q=Bogota&limit=1&appid=KEY
    GEOCODING_URL = os.getenv("OPENWEATHER_GEOCODING_URL")
    
    # URL de la API de Weather (obtener datos meteorológicos)
    # Documentación: https://openweathermap.org/current
    # Ejemplo: http://api.openweathermap.org/data/2.5/weather?lat=4.6&lon=-74&appid=KEY
    WEATHER_URL = os.getenv("OPENWEATHER_WEATHER_URL")

    # =========================================================================
    # CONFIGURACIÓN DE LLAMADAS HTTP
    # =========================================================================
    
    # Tiempo máximo de espera para las peticiones HTTP (en segundos)
    # Si la API de OpenWeather no responde en este tiempo, se lanza un error
    # Un valor muy bajo puede causar errores en redes lentas
    # Un valor muy alto puede hacer que la aplicación parezca "colgada"
    TIMEOUT_SECONDS = 10
    
    # Sistema de unidades para la temperatura
    # Opciones disponibles:
    # - "metric": Celsius (°C) - Sistema métrico
    # - "imperial": Fahrenheit (°F) - Sistema imperial (usado en USA)
    # - "standard": Kelvin (K) - Sistema científico
    UNITS = "metric"
    
    # Idioma para las descripciones del clima
    # Códigos de idioma soportados: es, en, fr, de, pt, it, ru, zh_cn, ja, etc.
    # Lista completa: https://openweathermap.org/current#multi
    # Con "es", las descripciones vendrán en español: "cielo claro", "lluvia ligera"
    LANGUAGE = "es"