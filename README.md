# HoosHousing


## Description
HoosHousing is a web application designed to provide a platform for University of Virginia students to submit reports and complaints about occurings in UVA's on-campus housing. It offers an intuitive interface for users to create reports and provide incident details. Additionally, whistleblowers can receive status updates and comments regarding their report's resolution. They can also interact with reports from others, if they have been made public, and upvote reports they deem important or urgent.

## Installation
```bash
# Clone the repository
git clone https://github.com/uva-cs3240-s24/project-b-26
cd project-b-26

# Set up a virtual environment (optional, but recommended)
python -m venv venv
source venv/bin/activate  # For MacOS
venv\Scripts\activate  # For Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations to create database schema
python manage.py migrate

# Start the server (from main project directory)
python manage.py runserver
