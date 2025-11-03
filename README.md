# LessonDjangoProject

Django project with catalog app with two test html pages home and contact

## Installation:

For work in program need to clone repos 
```
https://github.com/olex108/LessonDjangoProject.git
```
install dependencies from `pyproject.toml`

For work create file `.env` with params of django settings.py:

```
SECRET_KEY=your-secret-key
DEBUG=Debug param
```

For work create PostgresDB database and add params to file `.env`

```
NAME=name_of_catalog_database
USER=name_of_Postgress_DB_user
PASSWORD=password
HOST=host
PORT=port
```

## Description of Functionality

### functions in view.py of catalop app

- `home` Function to render the home page with GET request

- `products_list` Function to render all products list from database with GET request

- `product_info` Function to render all info of product by product_id with GET request

- `categories` Function to render all categories of products from database with GET request

- `contacts` Function to render contact page wits GET and POST requests


## Description models of DB

- `Category` Model representing a category. Model has field id with is not indicated witch is primary key for model and ForeignKey for model Product

```    
    id: pk of category
    name: name 
    description: description of category
```

- `Product` Model representing a product with fields 

```    
    id: pk of product
    name: name 
    description: details about product
    image: path to image file 
    category: ForeignKey of Category 
    price: price
    created_at: date time info about creation of product
    updated_at: lust update of product
```