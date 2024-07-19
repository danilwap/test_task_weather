from fastapi import FastAPI



app = FastAPI(title='Приложение погоды')

@app.get("/get_weather/{town}")
async def get_weather(town: str):
    pass