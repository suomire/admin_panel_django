# Репозиторий для образа сервиса панели администратора
`.env_example` находится в `config/.env_example` и для простоты полностью соответствует требуемому. 

1. Собрать образ
```commandline
docker build -t suomire/admin_web_static:1.1 .
```
2. Запушить образ
```commandline
docker push suomire/admin_web_static:1.1
```
