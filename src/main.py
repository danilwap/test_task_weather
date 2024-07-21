from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pages.router import router_pages

app = FastAPI(title='Приложение погоды')
app.include_router(router_pages)


@app.get('/')
def page_start():
    return RedirectResponse('/forecast_weather')

