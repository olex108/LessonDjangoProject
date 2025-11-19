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

For correct sending email add params to file `.env`

```
EMAIL_ADDRESS=e-mail_address
APP_EMAIL_PASSWORD=app_e-mail_password
```


## Description of Functionality

### CBV in view.py of catalog app

- `HomeView` CBV for render home page with pagination of products

- `ProductsListView` CBV for render all products list from database with GET request

- `ProductDetailView` CBV for render product detail page with GET request

- `CategoriesListView` CBV for render all categories list from database with GET request

- `ContactsView` Class to render contact information about company and form to fill user contacts and message

### CBV in view.py of blog app

- `PostsListView` CBV for render posts list view

- `PostDetailView` CBV for render post detail view

- `PostCreateView` CBV for create post view

- `PostUpdateView` CBV for update post view

- `PostDeleteView` CBV for delete post view



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

- `Contacts` Model representing a contacts of company with fields

```    
    id: pk of contact
    name: name
    email: email
    phone: phone number
```

- `ClientMessage` Model representing a message of client, for save contacts of client, save message and field is_answered to keep

```    
    id: pk of contact
    name: name
    phone: phone
    message: message
    created_at: date time info about creation of message
    is_answered: information about answer
```

- `Post` Model representing a blog post, for save contacts of client, save message and field is_answered to keep

```    
    id: pk of contact
    title: post title
    content: text of post
    image: path to image file 
    created_at: date time info about creation of message
    is_published: information about ready for publication
    views_counter: count of views
```