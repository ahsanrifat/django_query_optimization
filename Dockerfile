FROM python

RUN adduser --system rifat 
 
RUN mkdir app
RUN chown rifat: /app

WORKDIR /app
RUN mkdir data
RUN mkdir data/db

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV db_user=postgres
ENV db_pass=root

EXPOSE 8000

USER rifat


# ENTRYPOINT ["sh","entrypoint.sh"]

