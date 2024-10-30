# TomaCare - Backend

## Installation
- Create virtual environment using python.
  ```bash
  python -m venv .venv
  ```
  Activate the virtual environment:
  - Windows:
    ```bash
    .venv\Scripts\activate
    ```
  - Linux:
    ```bash
    source .venv/bin/activate
    ```
- Install all required Python packages.
  ```bash
  pip install -r requirements.txt
  ```
- Set Up the Database.
  - Ensure MySQL is running.
  - Create a database named `tomacare`.
    ```sql
    CREATE DATABASE tomacare;
    ```
- Create `.env` file with this template. _Change `USER`, `PASS`, and `HOST`_
  ```bash
  DATABASE_URL=mysql+pymysql://USER:PASS@HOST/tomacare
  ```
- Run database migration.
  ```bash
  alembic upgrade head
  ```