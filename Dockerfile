FROM python:3.7

WORKDIR /admin_movies

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "entrypoint.sh"]