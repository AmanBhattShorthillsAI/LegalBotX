# LegalBotX

A simple Django project for uploading and managing SCN files via a REST API.

## Features

- Upload SCN files through a REST API endpoint
- Stores uploaded files and timestamps

## Requirements

- Python 3.8+
- Django 5.2.4
- djangorestframework

## Installation

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd legalbotx
   ```
2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```
5. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

## Usage

- The API endpoint for uploading SCN files is available at:

  ```
  POST /api/upload/
  ```

  Use a tool like Postman or `curl` to upload files using the `file` field.
- Admin interface is available at `/admin/`.

## Project Structure

- `scn/` - Django app for SCN file uploads
- `legalbotx/` - Project settings and configuration
