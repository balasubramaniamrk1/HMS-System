# HMS Project Technology Stack

## 1. Backend
*   **Language**: Python
*   **Framework**: Django (Version 5.2.9)
    *   *Note: Version 5.2.9 is specified in requirements, though typically stable releases are 4.2 LTS or 5.0/5.1.*
*   **Server**: Gunicorn 21.2.0 (WSGI HTTP Server)
*   **Asynchronous Support**: asgiref 3.11.0

## 2. Database
*   **Primary Database**: PostgreSQL (Version 15)
*   **Adapter**: psycopg2-binary 2.9.11
*   **ORM**: Django ORM

## 3. Frontend
*   **Templating Engine**: Django Template Language (DTL)
*   **Styling**: Custom CSS
*   **Admin Interface**: Django Jazzmin 3.0.1 (Customizable Admin Theme)

## 4. Infrastructure & DevOps
*   **Containerization**: Docker & Docker Compose
*   **Environment Management**: python-dotenv 1.2.1
*   **Web Server (Production)**: Nginx (Typically used with Gunicorn, implied by production troubleshooting logs though not explicitly seen in root docker-compose yet)

## 5. Key Libraries
*   **Pillow 12.0.0**: Python Imaging Library (fork) for generic image processing capabilities.
*   **sqlparse 0.5.4**: Non-validating SQL parser for Python.
