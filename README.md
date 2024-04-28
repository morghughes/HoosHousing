# HoosHousing


## Description


## Installation
```bash
# Clone the repository
git clone https://github.com/uva-cs3240-s24/project-b-26
cd project-b-26

# Set up a virtual environment (optional, but recommended)
python -m venv venv
source venv/bin/activate  # For _MacOS_
venv\Scripts\activate  # For _Windows_

# Install dependencies
pip install -r requirements.txt

# Run migrations to create database schema
python manage.py migrate

# Start the server
python manage.py runserver
