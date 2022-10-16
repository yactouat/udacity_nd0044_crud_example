# basic CRUD example

## Introduction

This project consists of a basic CRUD app' built with Flask so that you have a working example of how to implement them. The app' is far from perfect so feel free to contribute !

It consists of 3 CRUDabble entities:

- a base item, that can have start and end dates
- a parent list of type `A` that can contain base items
- a parent list of type `B` that can contain base items
- both lists can have 0-to-many counterpart lists, so it's **many-to-many** relationship between them

## Tech Stack (Dependencies)

### 1. Backend Dependencies

Our tech stack will include the following:

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations

## Main Files: Project Structure

```sh
├── README.md
├── app.py *** the main driver of the app., includes SQLAlchemy models.
                "python app.py" to run after installing dependencies
                OR "docker compose up"
├── config.py *** Database URLs, CSRF generation, etc
├── error.log
├── forms.py *** Your forms
├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt" OR auto included from Dockerfile
├── static
│   ├── css 
│   ├── font
│   ├── ico
│   ├── img
│   └── js
└── templates
    ├── errors
    ├── forms
    ├── layouts
    └── pages
```

Overall:

* Controllers and Models are located in `app.py`.
* The web frontend is located in `templates/`, which references static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`

Files and folders:

* `templates/pages` -- Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages represent the data to the user.
* `templates/layouts` -- Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` -- Defines the forms used to create new items and parent items lists.
* `app.py` -- Defines routes that match the user’s URL, and controllers which handle data and renders views to the user. This is the main file to connect to and manipulate the database and render views with data to the user, based on the URL.
* Models in `app.py` -- Defines the data models that set up the database tables.
* `config.py` -- Stores configuration variables and instructions, separate from the main application code. This is where you connect to the database.

## Data Handling with `Flask-WTF` Forms

We use an interactive form builder library called [Flask-WTF](https://flask-wtf.readthedocs.io/). This library provides useful functionality, such as form validation and error handling. You can peruse the form builders in `forms.py` file. The WTForms are instantiated in the `app.py` file. To manage the request from Flask-WTF form, each field from the form has a `data` attribute on the frontend containing the value from user input.

## Development Setup

### with Docker

```bash
docker compose up
```

Navigate to project homepage [http://127.0.0.1/](http://127.0.0.1/) or [http://localhost](http://localhost)

### without Docker

* **Initialize and activate a virtualenv using:**

```bash
python -m virtualenv env
source env/bin/activate
```

>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command itemn below:

```bash
source env/Scripts/activate
```

* **Install the dependencies:**

```bash
pip install -r requirements.txt
```

* **Run the development server:**

```bash
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

* **Verify on the Browser**

Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000)
