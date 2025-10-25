FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/streamlit/streamlit-example.git



COPY ./requirements.txt requirements.txt
COPY ./app.py app.py

RUN pip install -r requirements.txt

EXPOSE 8501

ENTRY_POINT ["streamlit", "run"]

CMD ["app.py"]

