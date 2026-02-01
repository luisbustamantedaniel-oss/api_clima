# Weather API - Documentación del Contrato de API

## Descripción General

### ¿Qué hace la API?
Esta aplicación consume la **API de OpenWeatherMap** para obtener información meteorológica en tiempo real de cualquier ciudad del mundo. La aplicación actúa como un intermediario que simplifica el acceso a los datos climáticos.

### ¿Qué información devuelve?
- **Nombre de la ciudad** consultada
- **Temperatura actual** en grados Celsius
- **Humedad relativa** en porcentaje (0-100%)
- **Descripción del clima** en español (ej: "cielo claro", "nubes dispersas")

### ¿Para qué sirve?
- Consultar las condiciones climáticas actuales de cualquier ubicación
- Integrar datos meteorológicos en aplicaciones web o móviles
- Obtener información relevante para planificación de actividades

---

## Endpoints Utilizados

La aplicación utiliza dos endpoints de la API de OpenWeatherMap:

---

### 1. Geocoding API (Conversión de Ciudad a Coordenadas)

| Campo | Descripción |
|-------|-------------|
| **URL del endpoint** | `http://api.openweathermap.org/geo/1.0/direct` |
| **Método HTTP** | `GET` |
| **Documentación oficial** | [OpenWeather Geocoding API](https://openweathermap.org/api/geocoding-api) |

#### Parámetros Requeridos

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `q` | string | ✅ Sí | Nombre de la ciudad a buscar (ej: "Bogota", "Madrid") |
| `limit` | int | ❌ No | Número máximo de resultados (usamos 1) |
| `appid` | string | ✅ Sí | API Key de OpenWeatherMap |

#### Ejemplo de Petición

```http
GET http://api.openweathermap.org/geo/1.0/direct?q=Bogota&limit=1&appid=TU_API_KEY
```

#### Ejemplo de Respuesta Exitosa (JSON)

```json
[
  {
    "name": "Bogotá",
    "local_names": {
      "es": "Bogotá",
      "en": "Bogota"
    },
    "lat": 4.6097,
    "lon": -74.0817,
    "country": "CO",
    "state": "Bogota D.C."
  }
]
```

#### Descripción de Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | string | Nombre oficial de la ciudad |
| `lat` | float | Latitud de la ciudad |
| `lon` | float | Longitud de la ciudad |
| `country` | string | Código del país (ISO 3166) |
| `state` | string | Estado o departamento |

---

### 2. Current Weather API (Datos Meteorológicos)

| Campo | Descripción |
|-------|-------------|
| **URL del endpoint** | `http://api.openweathermap.org/data/2.5/weather` |
| **Método HTTP** | `GET` |
| **Documentación oficial** | [OpenWeather Current Weather](https://openweathermap.org/current) |

#### Parámetros Requeridos

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `lat` | float | ✅ Sí | Latitud de la ubicación |
| `lon` | float | ✅ Sí | Longitud de la ubicación |
| `appid` | string | ✅ Sí | API Key de OpenWeatherMap |
| `units` | string | ❌ No | Sistema de unidades: `metric` (Celsius), `imperial` (Fahrenheit), `standard` (Kelvin) |
| `lang` | string | ❌ No | Idioma de las descripciones (ej: `es` para español) |

#### Ejemplo de Petición

```http
GET http://api.openweathermap.org/data/2.5/weather?lat=4.6097&lon=-74.0817&appid=TU_API_KEY&units=metric&lang=es
```

#### Ejemplo de Respuesta Exitosa (JSON)

```json
{
  "coord": {
    "lon": -74.0817,
    "lat": 4.6097
  },
  "weather": [
    {
      "id": 802,
      "main": "Clouds",
      "description": "nubes dispersas",
      "icon": "03d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 18.5,
    "feels_like": 18.2,
    "temp_min": 17.0,
    "temp_max": 20.0,
    "pressure": 1015,
    "humidity": 72
  },
  "visibility": 10000,
  "wind": {
    "speed": 3.5,
    "deg": 180
  },
  "clouds": {
    "all": 40
  },
  "dt": 1706648400,
  "sys": {
    "type": 2,
    "id": 2035648,
    "country": "CO",
    "sunrise": 1706610000,
    "sunset": 1706653200
  },
  "timezone": -18000,
  "id": 3688689,
  "name": "Bogotá",
  "cod": 200
}
```

#### Descripción de los Campos Más Importantes

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `main.temp` | float | Temperatura actual en la unidad configurada (Celsius) |
| `main.humidity` | int | Humedad relativa en porcentaje (0-100) |
| `main.feels_like` | float | Sensación térmica |
| `main.temp_min` | float | Temperatura mínima del momento |
| `main.temp_max` | float | Temperatura máxima del momento |
| `main.pressure` | int | Presión atmosférica en hPa |
| `weather[0].description` | string | Descripción textual del clima (en español si se configura `lang=es`) |
| `weather[0].main` | string | Grupo principal del clima (Clouds, Rain, Clear, etc.) |
| `weather[0].icon` | string | Código del ícono del clima |
| `wind.speed` | float | 💨 Velocidad del viento en m/s |
| `name` | string | Nombre de la ciudad |
| `sys.country` | string | Código del país |

---

## Manejo de Errores

### Códigos de Error Posibles

| Código HTTP | Significado | Causa Común |
|-------------|-------------|-------------|
| `400` | Bad Request | Parámetros inválidos o faltantes |
| `401` | Unauthorized | API Key inválida o no proporcionada |
| `404` | Not Found | Ciudad no encontrada |
| `429` | Too Many Requests | Límite de peticiones excedido |
| `500` | Internal Server Error | Error interno del servidor de OpenWeather |
| `503` | Service Unavailable | Servicio temporalmente no disponible |

---

### Ejemplo de Respuesta de Error (Ciudad No Encontrada)

**Petición:**
```http
GET http://api.openweathermap.org/geo/1.0/direct?q=CiudadInexistente&limit=1&appid=TU_API_KEY
```

**Respuesta:**
```json
[]
```

**Explicación:** Cuando la ciudad no existe, la API de Geocoding devuelve un array vacío. Nuestra aplicación lo detecta y responde con:

```json
{
  "detail": "Ciudad 'CiudadInexistente' no encontrada. Verifica el nombre e intenta de nuevo."
}
```

---

### Ejemplo de Error de API Key Inválida

**Petición:**
```http
GET http://api.openweathermap.org/data/2.5/weather?lat=4.6&lon=-74&appid=API_KEY_INVALIDA
```

**Respuesta:**
```json
{
  "cod": 401,
  "message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."
}
```

**Explicación:** La API Key proporcionada no es válida o no se ha activado aún. Las nuevas API Keys pueden tardar hasta 2 horas en activarse después de generarse.

---

### Ejemplo de Error de Límite de Peticiones Excedido

**Respuesta:**
```json
{
  "cod": 429,
  "message": "Your account is temporary blocked due to exceeding of requests limitation of your subscription type."
}
```

**Explicación:** Se ha excedido el límite de llamadas por minuto/mes según el plan suscrito. El plan gratuito permite 60 llamadas/minuto y 1,000,000 llamadas/mes.

---

## Endpoint de la Aplicación Local

### Obtener Clima de una Ciudad

| Campo | Descripción |
|-------|-------------|
| **URL** | `http://localhost:8000/api/weather/{city}` |
| **Método HTTP** | `GET` |

#### Ejemplo de Petición

```http
GET http://localhost:8000/api/weather/Bogota
```

#### Ejemplo de Respuesta Exitosa

```json
{
  "city": "Bogota",
  "temperature": 18.5,
  "humidity": 72,
  "description": "nubes dispersas"
}
```

#### Campos de Respuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `city` | string | Nombre de la ciudad consultada |
| `temperature` | float | Temperatura en grados Celsius |
| `humidity` | int | Porcentaje de humedad (0-100) |
| `description` | string | Descripción del clima en español |

---

## Configuración Requerida

### Variables de Entorno (.env)

```env
OPENWEATHER_API_KEY=tu_api_key_aquí
OPENWEATHER_GEOCODING_URL=http://api.openweathermap.org/geo/1.0/direct
OPENWEATHER_WEATHER_URL=http://api.openweathermap.org/data/2.5/weather
```

### Obtener API Key

1. Registrarse en [OpenWeatherMap](https://openweathermap.org/api)
2. Ir a "My API Keys" en el perfil
3. Generar una nueva API Key (puede tardar hasta 2 horas en activarse)

---

## Recursos Adicionales

- [Documentación oficial de OpenWeatherMap](https://openweathermap.org/api)
- [Geocoding API Docs](https://openweathermap.org/api/geocoding-api)
- [Current Weather API Docs](https://openweathermap.org/current)
- [Códigos de idioma soportados](https://openweathermap.org/current#multi)
- [FAQ de errores](https://openweathermap.org/faq)

---

## 👤 Autor

- **Nombre:** Ing. Eduardo Pimienta
- **Fecha:** Enero 2026

---

## Licencia

MIT License
