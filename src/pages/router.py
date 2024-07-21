from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from weather.utils import get_coordinates, get_forecast, get_forecast_weather

router_pages = APIRouter(prefix="/forecast_weather")

templates = Jinja2Templates(directory='templates')


@router_pages.get("/")
def get_base_page(request: Request):
    return templates.TemplateResponse("forecast_weather.html", {'request': request})


@router_pages.get("/{city}")
def get_weather(request: Request, weathers=Depends(get_forecast_weather)):
    return templates.TemplateResponse("forecast_weather.html", {"request": request, "weathers": weathers})