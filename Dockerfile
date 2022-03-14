FROM python:alpine
RUN addgroup app && adduser -S -G app app
USER app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py shell
ENV db_user=postgres
ENV db_pass=root