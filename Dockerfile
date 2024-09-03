FROM python:3.9.7

WORKDIR /usr/src/app

#./ because our current directory is /user/scr/app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Same as uvicorn app.main:app --host 0.0.0.0 --port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



# Commands to run 
# docker build -t fastapi .
# docker-compose up -d
# do the following in another terminal:
    # docker-compose exec api alembic upgrade head
# When customizing docker-compose file names we do:
# docker-compose -f docker-compose-newname.yml up -d
# example:
# docker-compose -f docker-compose-dev.yml up -d
# compose down example:
# docker-compose -f docker-compose-dev.yml down 


# pushing to dockerhub
# docker image tag api-api stevenmelensen/fastapi
# docker push stevenmelensen/fastapi:api-api

# docker image: api-api-1