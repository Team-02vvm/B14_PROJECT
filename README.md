# B14_PROJECT
Skin Disease Classification Web Application

This project integrates OpenCV for image processing and Django for web development to classify skin diseases. Using Random Forest with Incremental PCA for dimensionality reduction, the model achieved an accuracy of 82.16%. The application demonstrates the potential of creating user-friendly, scalable tools for early skin disease detection in healthcare.

Project Overview

1. Frontend: HTML templates styled with internal CSS for the web interface.


2. Backend: Django framework with Python for routing, logic, and database management.


3. Machine Learning: Random Forest Classifier with Incremental PCA for dimensionality reduction.


4. Database: SQLite for storing user authentication and session data.




---

Prerequisites

Python 3.x

Django 4.x or later

OpenCV

SQLite


Installation

1. Clone the Repository

git clone <repository-url>  
cd skin-disease-classification


2. Create Virtual Environment

python -m venv venv  
source venv/bin/activate  # For Linux/macOS  
venv\Scripts\activate     # For Windows


3. Install Dependencies

pip install django opencv-python numpy scikit-learn


4. Run Migrations

python manage.py migrate


5. Start the Server

python manage.py runserver




---

Creating the Django App

Step 1: Create a New App

django-admin startapp demopage

Step 2: Update settings.py

Add the newly created app to INSTALLED_APPS:

INSTALLED_APPS = [  
    ...  
    'demopage',  
]

Step 3: Create HTML Template

1. Create a templates folder inside demopage.


2. Inside templates, create index.html and add your HTML structure using the following:

<!DOCTYPE html>  
<html lang="en">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>Skin Disease Classifier</title>  
</head>  
<body>  
    <h1>Welcome to Skin Disease Classification App</h1>  
</body>  
</html>



Step 4: Define Views

Edit views.py in demopage to create a view for the home page:

from django.shortcuts import render  

def home(request):  
    return render(request, 'index.html')

Step 5: Configure URLs

Edit urls.py in the main project folder to add the path for the home view:

from django.contrib import admin  
from django.urls import path  
from demopage import views  

urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('', views.home, name='index'),  
]


---

Database Setup

Initialize Database

Run the following command to set up the SQLite database:

python manage.py migrate

User Authentication

auth_group table: Stores information on user groups such as admin, agents, and regular users.

auth_user table: Stores predefined input fields such as username, password, first_name, last_name, etc.



---

Running the Application

1. Start the development server:

python manage.py runserver


2. Visit http://127.0.0.1:8000/ in your browser to access the application.




---

Features

Image Processing: Utilizes OpenCV for pre-processing images.

Machine Learning: Random Forest for classification with Incremental PCA for dimensionality reduction.

User Authentication: Built-in Django authentication system with SQLite backend.

Simple UI: HTML-based interface styled with internal CSS.



---

Future Work

Enhance the UI with improved styling and UX.

Integrate external CSS frameworks like Bootstrap.

Implement user registration and profile management.

Add more sophisticated ML models and evaluation metrics.


---

Acknowledgements

Django Documentation

OpenCV Documentation

Scikit-learn Documentation
