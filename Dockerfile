FROM python:3.12-slim
WORKDIR /app
COPY ingesta/requirements.txt ingesta/requirements.txt
COPY dbt/requirements.txt dbt/requirements.txt
COPY app/requirements.txt app/requirements.txt
RUN pip install --no-cache-dir -r ingesta/requirements.txt -r dbt/requirements.txt -r app/requirements.txt
COPY . .
CMD ["python", "pipeline.py"]
