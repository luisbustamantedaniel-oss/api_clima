"""
=============================================================================
DTOs (DATA TRANSFER OBJECTS) - MODELOS DE DATOS
=============================================================================

Este módulo contiene los DTOs (Data Transfer Objects) utilizados para
estructurar los datos de respuesta de la API.

¿Qué es un DTO?
---------------
Un DTO es un objeto que define la estructura de los datos que se transfieren
entre capas de la aplicación o hacia/desde clientes externos.

¿Por qué usar DTOs en FastAPI?
------------------------------
1. VALIDACIÓN AUTOMÁTICA: Pydantic valida que los datos cumplan el esquema
2. DOCUMENTACIÓN: FastAPI genera docs automáticos (Swagger) basados en los DTOs
3. SERIALIZACIÓN: Convierte automáticamente objetos Python a JSON
4. TYPE HINTS: Mejora el autocompletado y detección de errores en el IDE
5. CONSISTENCIA: Garantiza que todas las respuestas tengan el mismo formato

Ejemplo de respuesta generada:
{
    "city": "Bogota",
    "temperature": 18.5,
    "humidity": 72,
    "description": "nubes dispersas"
}

Autor: [Tu nombre]
Fecha: Enero 2026
=============================================================================
"""

# BaseModel es la clase base de Pydantic para definir modelos de datos
# Proporciona validación automática, serialización y documentación
from pydantic import BaseModel, Field


class WeatherResponseDTO(BaseModel):
    """
    DTO para la respuesta de clima.
    
    Este modelo define la estructura exacta de los datos que se devuelven
    cuando un usuario consulta el clima de una ciudad.
    
    Características:
    - Todos los campos son obligatorios (no tienen valor por defecto)
    - FastAPI valida automáticamente que los datos cumplan este esquema
    - Se genera documentación automática en Swagger UI
    
    Atributos:
        city (str): Nombre de la ciudad consultada
        temperature (float): Temperatura actual en grados Celsius
        humidity (int): Porcentaje de humedad relativa (0-100)
        description (str): Descripción textual del clima en español
    
    Ejemplo:
        >>> weather = WeatherResponseDTO(
        ...     city="Bogota",
        ...     temperature=18.5,
        ...     humidity=72,
        ...     description="nubes dispersas"
        ... )
        >>> weather.model_dump()  # Convierte a diccionario
        {'city': 'Bogota', 'temperature': 18.5, 'humidity': 72, 'description': 'nubes dispersas'}
    """

    # =========================================================================
    # CAMPO: city (nombre de la ciudad)
    # =========================================================================
    # Field(...) indica que el campo es OBLIGATORIO (el ... es el marcador)
    # El parámetro 'description' aparece en la documentación de Swagger
    city: str = Field(
        ...,  # ... significa que es un campo requerido (no tiene valor por defecto)
        description="Nombre de la ciudad consultada",
        examples=["Bogota", "Madrid", "Buenos Aires"]  # Ejemplos para la documentación
    )

    # =========================================================================
    # CAMPO: temperature (temperatura en Celsius)
    # =========================================================================
    # float permite valores decimales como 18.5, 20.3, etc.
    # La temperatura viene en Celsius porque configuramos units="metric" en AppSettings
    temperature: float = Field(
        ...,
        description="Temperatura actual en grados Celsius",
        examples=[18.5, 25.0, -5.2]
    )

    # =========================================================================
    # CAMPO: humidity (porcentaje de humedad)
    # =========================================================================
    # int porque la humedad siempre es un número entero (0-100)
    # ge=0 y le=100 podrían agregarse para validar el rango
    humidity: int = Field(
        ...,
        description="Porcentaje de humedad relativa (0-100%)",
        examples=[72, 45, 90]
    )

    # =========================================================================
    # CAMPO: description (descripción del clima)
    # =========================================================================
    # La descripción viene en español porque configuramos lang="es" en AppSettings
    # Ejemplos: "cielo claro", "nubes dispersas", "lluvia ligera"
    description: str = Field(
        ...,
        description="Descripción del clima actual en español",
        examples=["cielo claro", "nubes dispersas", "lluvia ligera", "tormenta"]
    )

    # =========================================================================
    # CONFIGURACIÓN DEL MODELO (opcional pero útil)
    # =========================================================================
    class Config:
        """
        Configuración adicional del modelo Pydantic.
        
        json_schema_extra: Permite agregar ejemplos completos que aparecen
                          en la documentación de Swagger UI.
        """
        json_schema_extra = {
            "example": {
                "city": "Bogota",
                "temperature": 18.5,
                "humidity": 72,
                "description": "nubes dispersas"
            }
        }