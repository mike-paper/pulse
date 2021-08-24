source ~/.bash_profile
docker build -t paperapi . && PORT=5000 && \
docker run -it -p ${PORT}:${PORT} \
--env-file .env \
-e PORT=${PORT} \
-e WORKERS=4 \
paperapi:latest