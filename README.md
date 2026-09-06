# TachoQuiz — Django Backend

TachoQuiz is a web application designed to help professional drivers practise tachograph rules, driving times, rest periods, and CPC-related knowledge.  
This repository contains the Django backend, responsible for authentication, database management, quiz logic, and integration with the existing frontend.

---

## 🚀 Project Overview

The backend is built using **Django**, with **PostgreSQL** prepared for production deployment.  
The project follows a structured development process based on **18 User Stories**.


---

## 🗂️ Technologies Used

- **Python 3.12**  
- **Django 6.1**  
- **psycopg 3.3.5 (binary)** 
- **python-decouple 3.8** 
- **SQLite3** (development database)  
- **PostgreSQL** (production database)  
- **asgiref**, **sqlparse**, **typing_extensions**
- **HTML, CSS, JavaScript** (existing frontend integration)  
- **Django Admin**  
- **WSL Ubuntu + VS Code**  
 

---

## 📦 Project Structure

tachoquiz-backend-django/
│
├── tachoquiz/          # Django project configuration
├── quiz/               # Main application
│   ├── models.py       # Category, Question, Answer models
│   ├── views.py        # Home, Register, Confirmation views
│   ├── forms.py        # RegistrationForm
│   ├── urls.py         # App routes
│   ├── templates/quiz/ # HTML templates
│   └── static/quiz/    # CSS, images
│
├── manage.py
└── requirements.txt

Code

---

# 🧩 Completed User Stories

---

## 🟦 US01 — Set Up Django Project

### Description
As a developer, I want to set up the Django project so that I have a working backend foundation for the TachoQuiz application.

### Implementation Summary
- Django project created (`tachoquiz`)
- Main application created (`quiz`)
- Application added to `INSTALLED_APPS`
- Development server runs successfully
- Standard Django project structure established
- `.gitignore` configured
- Sensitive files excluded from version control

### Status  
✔ Completed

---

## 🟦 US02 — Configure PostgreSQL Database

### Description
As a developer, I want the application to use PostgreSQL so that the database is suitable for production deployment.

### Implementation Summary
- PostgreSQL configuration prepared in `settings.py`
- Database connection tested
- Migrations applied successfully
- Application can create and retrieve records
- Environment variables prepared for production

### Status  
✔ Completed

---

## 🟦 US03 — Create Quiz Database Models

### Description
As an administrator, I want quiz categories, questions, and answers stored in the database so that quiz content can be managed dynamically.

### Implementation Summary

Three models were created:

#### Category
- name  
- slug  

#### Question
- category (ForeignKey)  
- text  
- explanation  

#### Answer
- question (ForeignKey)  
- text  
- is_correct  

### Additional Work
- Proper relationships established  
- `related_name` added  
- `__str__` methods implemented  
- Migrations created and applied  

### Status  
✔ Completed

---

## 🟦 US04 — Configure Django Admin

### Description
As an administrator, I want to manage quiz content through Django Admin so that I can add and update questions without modifying the source code.

### Implementation Summary
- Category, Question, and Answer models registered in Django Admin
- Admin supports:
  - Creating categories
  - Creating questions
  - Creating answers
  - Marking correct answers
  - Editing and deleting quiz content

### Status  
✔ Completed

---

## 🟦 US05 — User Registration

### Description
As a visitor, I want to create an account so that I can access personalised functionality.

### Implementation Summary
User registration was implemented using Django’s `UserCreationForm`, extended to include a required email field.

### What Was Added
- `RegistrationForm` with:
  - username  
  - email (required)  
  - password1  
  - password2  
- Validation for:
  - required email  
  - password mismatch  
  - weak passwords  
  - duplicate usernames  
- `register` view (GET + POST)
- `confirmation` view
- Templates:
  - `register.html`
  - `confirmation.html`
- Error messages displayed in the template
- Styling integrated with existing frontend design

### How It Works
1. User visits `/register/`
2. User fills in the registration form
3. Django validates the input
4. If valid:
   - A new user is created
   - User is redirected to the confirmation page
5. If invalid:
   - Errors are displayed beneath the form

### Files Modified
- `quiz/forms.py`
- `quiz/views.py`
- `quiz/templates/quiz/register.html`
- `quiz/templates/quiz/confirmation.html`
- `quiz/urls.py`

### Testing
- Registration with valid data → success  
- Short password → error  
- Password mismatch → error  
- Duplicate username → error  
- Invalid email → error  
- Confirmation page displays correctly  

### Status  
✔ Completed  

---

## 🧪 Testing Summary (US01–US05)

- Development server runs correctly  
- Models behave as expected  
- Django Admin fully functional  
- Registration workflow works end-to-end  
- Validation errors displayed correctly  
- Templates load with correct styling  
- Static files integrated successfully  

---

## US06 — User Authentication (Login, Logout & Register Integration)

### Description
As a user, I want to log in, log out, and register an account so that I can securely access personalised quiz functionality.

### Implementation Summary
User authentication was implemented using Django’s built-in authentication system.
All authentication pages were updated to match the existing UI, and several template and styling issues were fixed to ensure consistency across the application.

### What Was Added
- Login functionality using:
  - authenticate()
  - login()
- Logout functionality using:
  - logout()
  - success message via Django’s messaging framework
- Updated register.html to match the login page layout
- Dynamic navbar behaviour:
  - shows username when logged in
  - shows Login/Register when logged out
- Consistent input styling for:
  - username
  - email
  - password
- Error handling for:
  - invalid login
  - incorrect password
  - missing fields
  - registration errors
- Template inheritance fixes across all authentication pages

### How It Works
1. User visits `/login/` or `/register/`
2. User fills in the form
3. Django validates the credentials or registration data
4. If valid:
   - user is logged in OR account is created
   - logout displays a success message
   - user is redirected to the appropriate page
5. If invalid:
   - errors are displayed beneath the form
6. Navbar updates automatically based on authentication state


### Files Modified
- `quiz/views.py`
- `quiz/forms.py`
- `quiz/templates/tachoquiz/base.html`
- `quiz/templates/quiz/login.html`
- `quiz/templates/quiz/register.html`
- `quiz/templates/quiz/confirmation.html`
- `quiz/static/quiz/css/style.css`
- `quiz/urls.py`

### Testing
- Valid login → success  
- Invalid login → error message  
- Valid registration → account created  
- Password mismatch → error  
- Weak password → error  
- Duplicate username → error  
- Logout → success message displayed  
- Navbar updates correctly  
- Input fields consistent across login and register pages  

### Status
✔ Completed

---

### Bugs Encountered
- Template inheritance broken  
  - duplicated `<html>`, `<head>`, `<body>` tags in child templates  
  - fixed by ensuring all pages extend `base.html`

- Static files not loading  
  - missing `STATICFILES_DIRS` caused CSS not to load  
  - fixed by adding correct static configuration

- Register input fields too small  
  - Django-generated fields did not receive `.form-group` styling  
  - fixed by wrapping fields in `.form-group` and adding universal input CSS

- Navbar alignment issues  
  - username and links appeared in the wrong order  
  - fixed by reorganising `<li>` elements and improving UX

- Logout message not displayed  
  - missing message block in templates  
  - fixed by adding messages section in `base.html`