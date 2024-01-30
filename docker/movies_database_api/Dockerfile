FROM python:3.8
LABEL authors="alibashir"


COPY movies_database_api_requirements.txt /netflix_mimic_app/movies_database_api/movies_database_api_requirements.txt
RUN pip install --no-cache-dir -r /netflix_mimic_app/movies_database_api/movies_database_api_requirements.txt
RUN mkdir /secret
RUN openssl rand -hex 32 > /secret/key.txt
EXPOSE 8000
WORKDIR /netflix_mimic_app/movies_database_api/src
CMD ["uvicorn", "movies_api_main:app","--host","0.0.0.0", "--port", "8000", "--reload" ]
