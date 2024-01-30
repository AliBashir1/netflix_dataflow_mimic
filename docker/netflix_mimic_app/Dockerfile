FROM python:3.8
LABEL authors="alibashir"

COPY requirements.txt movies_app/movies_app_requirements.txt
RUN pip install --no-cache-dir -r /netflix_mimic_app/movies_app_requirements.txt
WORKDIR /movies_app/src
CMD ["python3", "main.py"]