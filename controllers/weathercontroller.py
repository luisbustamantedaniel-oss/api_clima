import httpx
from fastapi import APIRouter
from services.weatherservices import WeatherService
from DTOs.weatherDtos import WeatherResponseDTO

router = APIRouter(prefix="/api")

@router.get("/weather/{city}", response_model=WeatherResponseDTO)
async def get_weather(city: str):
    
    async with httpx.AsyncClient() as http_client:
        weather_service = WeatherService()
        weather_response = await weather_service.get_weather(city, http_client)
        return weather_response
    