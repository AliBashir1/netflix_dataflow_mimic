FROM python:3.8
LABEL authors="alibashir"

COPY netflic_mimic_app_requirements.txt netflix_mimic_app/netflic_mimic_app_requirements.txt
RUN pip install --no-cache-dir -r /netflix_mimic_app/netflic_mimic_app_requirements.txt
WORKDIR /movies_app/src
CMD ["python3", "main.py"]