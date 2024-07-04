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

# Please note that the "python" command depends on the version of Python you have installed on your local machine.
```
## Sources
- https://docs.djangoproject.com/en/stable/topics/testing/
- https://docs.djangoproject.com/en/stable/topics/settings/
- https://docs.github.com/en/actions
- https://docs.github.com/en/actions/security-guides/encrypted-secrets
- https://docs.djangoproject.com/en/stable/ref/databases/
- https://www.postgresql.org/about/advantages/
- https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-SECRET_KEY
- https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- https://testdriven.io/blog/django-ci-github-actions/
- https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
- https://developer.mozilla.org/en-US/docs/Learn/CSS/Styling_text/Fundamentals
- https://cssgradient.io/
- https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Introduction
- https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Home_page
- https://developers.google.com/identity/branding-guidelines
- https://docs.djangoproject.com/en/3.2/topics/auth/customizing/
- https://docs.github.com/en/actions/learn-github-actions/environment-variables
- https://docs.djangoproject.com/en/3.2/topics/testing/tools/
- https://docs.github.com/en/actions/reference/encrypted-secrets
- https://help.github.com/en/github/automating-your-workflow-with-github-actions/configuring-a-workflow
- https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
- https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
- https://www.djangoproject.com/weblog/2020/feb/03/security-releases/
- https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html
- https://testdriven.io/blog/django-custom-user-model/
- https://docs.github.com/en/actions/managing-workflow-runs/re-running-workflows-and-jobs

