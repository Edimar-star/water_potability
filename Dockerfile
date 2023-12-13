FROM python:latest

WORKDIR /app

RUN pip install virtualenv
RUN virtualenv venv
RUN /bin/bash -c "source venv/bin/activate"

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN chmod +x entrypoint.sh

EXPOSE 3000 8501

CMD ["./entrypoint.sh"]
