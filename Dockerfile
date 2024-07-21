FROM python
LABEL authors="Данила Бескроков"

COPY . .

RUN pip install -r requirements.txt
WORKDIR /src
CMD ["uvicorn", "main:app", "--port", "80"]