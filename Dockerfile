FROM python:alpine
# RUN addgroup rifat && adduser -S -G rifat rifat
# USER rifat
WORKDIR /app
RUN mkdir data
RUN mkdir data/db
# so user usr has the persmission to write data in data directory
# so if a volume is there named orm_vol
# then run docker run -it -p 8000:8000 -v orm_vol:/app/data orm
# RUN mkdir data [permission error --> find out the reason]
COPY requirements.txt .
RUN pip install -r requirements.txt
# COPY entry.sh .
COPY . .
# CMD python manage.py shell_plus --ipython
ENV db_user=postgres
ENV db_pass=root
EXPOSE 8000
