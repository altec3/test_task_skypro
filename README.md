### Тестовое задание
#### Для прохождения в "Центр Карьеры" SkyPro 
*Стек: python:3.10, Django:4.1.7, Postgres:12.4*
####
### Описание задания

---

`Цель работы`  
* Создать веб-приложение, с API интерфейсом и админ-панелью.
* Создать базу данных, используя миграции Django.  

`Документация`  

Документация доступна по адресу: [http://localhost:8000/api/schema/swagger-ui](http://localhost:8000/api/schema/swagger-ui)
### Для проверки задания:

---

1. Создать и запустить образа с PostgreSQL

```python
docker run --name psql -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:12.4-latest
```

2. Применить миграции к базе данных

```python
python manage.py migrate
```

3. Загрузить фикстуры в базу данных

```python
python manage.py loaddata network.json
```
