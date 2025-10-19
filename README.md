# LessonDjangoProject

Django project with catalog app with two test html pages home and contact

## Installation:

For work in program need to clone repos 
```
https://github.com/olex108/LessonDjangoProject.git
```
and install dependencies from `pyproject.toml`

For work create file `.env` with params of django settings.py:

```
SECRET_KEY=your-secret-key

DEBUG=True
```

## Description of Functionality

### functions in view.py of catalop app

- `home` Function to render the home page with GET request

- `contacts` Function to render contact page wits GET and POST requests