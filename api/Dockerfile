FROM python:3.8-alpine

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app/

# RUN pip install /app/

WORKDIR /app/

EXPOSE 8080

ENTRYPOINT ["uvicorn", "main:app"]
CMD ["--host", "0.0.0.0", "--port", "8080", "--workers", "4"]