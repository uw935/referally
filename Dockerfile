FROM python:3.11.12-slim

WORKDIR /build/

COPY /src/ /build/
COPY .env /build/
COPY requirements.txt /build/

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN alembic upgrade head

CMD ["python3", "-m", "referally.main"]
