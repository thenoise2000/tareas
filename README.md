Api rest para la gestion de tareas usando Django con Celery Se desarrollo una API REST para operaciones de CRUD con Django empleando celery y redis.

Herramientas:

- Django

- Celery

- AWS

- Redis

- PostgreSQL

- Html

- CSS

- Swagger

- Postman



Preview

/////////// Pagina de Login ////////////////

![image alt](https://github.com/thenoise2000/tareas/blob/main/docs/Login.jpg?raw=true)

Admin app

![image alt](https://github.com/thenoise2000/tareas/blob/main/docs/panel.jpg?raw=true)

/////////// Como funciona /////////////////////

![image alt](https://github.com/thenoise2000/tareas/blob/main/docs/redis.png?raw=true)

///////////// Flujo de ejecucion //////////////////

![image alt](https://github.com/thenoise2000/tareas/blob/main/docs/worker.jpg?raw=true)

Pasos para configurar y ejecutar

1 - Crea el entorno virtual

    ```bash
    python -m virtualenv venv
    ```
2 - Activado:
    
    ```bash
    cd .\venv\Scripts\activate
    ```

3 - Instala las dependencias ->  requirements.txt:

    ```bash
    pip install -r requirements.txt
    ```

4-  Crea y Configura un archivo de entorno .env en la raiz del proyecto

5 - Instala Redis https://redis.io/download/
   
6- Migrar el proyecto

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7 - Para ejecutar el proyecto

    ```bash
    python manage.py runserver
    ```
    
8 - Crear Superusuario

    ```bash
    python manage.py createsuperuser
    ```

9 - Ejecuta Celery 
    ```bash
    celery -A gestor_tareas worker -l info -E
    ```

Para implementar la funcionalidad solicitada en Django, podemos seguir los siguientes pasos:

Definir las Entidades: Crear los modelos en Django que representen las entidades Task, User y Sender Product , con sus atributos y relaciones correspondientes.

Definir las visatas: Crear funciones en las vistas correspondientes para cada entidad que permitan acceder a los datos en la base de datos.

Implementar el Servicio de gestion de Tareas: Crear un servicio que contenga la lógica para gestionar el crud aplicables según los parámetros de entrada recibidos.

Crear el Controlador REST: Implementar un controlador REST en Django que exponga los endpoints para la las operaciones.
