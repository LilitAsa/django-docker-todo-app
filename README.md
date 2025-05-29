# Django Docker ToDo Application

## Description

This is a simple ToDo application built using the Django web framework. The application is containerized using Docker Compose, with services for the Django application (running with Gunicorn), a PostgreSQL database, and Nginx as a reverse proxy and static file server. It includes basic user authentication and task management features.

## Technologies Used

*   **Django:** Python web framework
*   **PostgreSQL:** Relational database
*   **Gunicorn:** Python WSGI HTTP Server
*   **Nginx:** Web server and reverse proxy
*   **Docker Compose:** Tool for defining and running multi-container Docker applications
*   **Adminer:** Database management tool (optional, included for convenience)

## Prerequisites

*   Docker and Docker Compose installed on your machine.

## Getting Started

1.  **Clone the repository** :
    ```bash
    git clone https://github.com/LilitAsa/django-docker-todo-app.git
    cd todo
    ```

2.  **Create a `.env` file:**
    Create a file named `.env` in the root of the project directory and add your database credentials and Django secret key. Replace the placeholder values with your actual desired settings.

    ```env
    SECRET_KEY=your_django_secret_key_here
    DEBUG=True
    ALLOWED_HOSTS=localhost 127.0.0.1

    # Database settings
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=postgres
    DB_PORT=5432
    ```
    **Note:** For production, set `DEBUG=False` and configure `ALLOWED_HOSTS` appropriately.

3.  **Build and run the Docker containers:**
    Navigate to the root directory of the project in your terminal and run:
    ```bash
    docker compose up --build -d
    ```
    The `-d` flag runs the containers in detached mode (in the background).

4.  **Apply database migrations:**
    Once the containers are running, execute the Django migrations to create the database tables:
    ```bash
    docker compose exec todo python manage.py migrate
    ```

5.  **Collect static files:**
    Collect the static files for Nginx to serve:
    ```bash
    docker compose exec todo python manage.py collectstatic --noinput
    ```

6.  **Create a Django superuser (optional):**
    To access the Django admin panel, create a superuser:
    ```bash
    docker compose exec todo python manage.py createsuperuser
    ```
    Follow the prompts to create a username and password.

## Accessing the Application

The application should now be running and accessible in your web browser:

*   **ToDo App:** `http://localhost/`
*   **Django Admin:** `http://localhost/admin/` (Use the superuser credentials you created)
*   **Adminer:** `http://localhost:8888/` (Connect to the `postgres` service using your `.env` credentials)

## Stopping the Application

To stop the running containers, navigate to the project's root directory in the terminal and run:
```bash
docker compose down
```
To stop and remove the containers, networks, and volumes (including database data), use:
```bash
docker compose down -v
```

## Project Structure

```
.
├── base/               # Django project settings and root urls
├── main/               # Main Django app
├── users/              # Users app (authentication, profiles, tasks)
├── static/             # Static files (CSS, JS, images)
├── media/              # Media files (user uploads)
├── logs/               # Application logs
├── compose.yaml        # Docker Compose configuration
├── dockerfile          # Dockerfile for the Django application
├── nginx.conf          # Nginx configuration
├── requirements.txt    # Python dependencies
├── gunicorn.py         # Gunicorn configuration
├── .env                # Environment variables (create this file)
└── manage.py           # Django management script


