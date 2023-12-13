FROM python:latest

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x entrypoint.sh

EXPOSE 3000 8501

CMD ["./entrypoint.sh"]
