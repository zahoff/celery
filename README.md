## Запуск

### Запуск недокеризированного (почти) приложения: 

1. Создаём виртуальное окружение, устанавливаем зависимости 
2. Запускаем redis
```bash
docker-compose up
```
3. Запускаем celery 
```bash
celery -A upscale_task.celery worker --loglevel=info
```
4. Запускаем файл `flask_app.py`
5. Отправляем запросы, запустив файл `client.py`

Должен получиться вывод вроде такого: 
```
{'task_id': 'fcdd0c4d-c755-46cd-82e8-de9deecded69'}
{'link': 'link is not ready yet', 'status': 'PENDING'}
{'link': 'link is not ready yet', 'status': 'PENDING'}
{'link': 'link is not ready yet', 'status': 'PENDING'}
{'link': 'link is not ready yet', 'status': 'PENDING'}
{'link': 'link is not ready yet', 'status': 'PENDING'}
{'link': 'http://127.0.0.1:5000/processed/lama_600px.png', 'status': 'SUCCESS'}
```


### Запуск докеризированного приложения:
(сервер у меня конкретно не всегда принимает запросы, проблему не удалось на данный момент устранить (возможно, из-за использования WSL), поэтому не предлагается как единственный вариант для запуска)

1. Раскомментировать весь код в `docker-compose.yml`
2. Раскомментировать нижний celery и закомментировать верхний celery в `upscale_task.py`, чтобы получилось так:
```python 
# celery = Celery(
#     'upscaling',
#     backend=('redis://127.0.0.1:6379/1'),
#     broker=('redis://127.0.0.1:6379/2')
# )

celery = Celery(
    'upscaling',
    backend=os.getenv('BACKEND'),
    broker=os.getenv('BROKER')
)
```
3. Запускаем контейнер 
```bash 
docker-compose up
```
ИЛИ по отдельности в разных терминалах 
```bash 
docker-compose up redis
```
```bash 
docker-compose up celery
```
```bash
docker-compose up app
```
