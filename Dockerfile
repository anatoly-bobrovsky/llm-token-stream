FROM python:3.13-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /src
WORKDIR /src

EXPOSE 8000

CMD [ "python", "api_app.py" ]
