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


## US07 — Display Quiz Categories

### Description

As a user, I want to see available quiz categories so that I can choose the topic I want to practice.

### Implementation Summary

Quiz categories are now retrieved dynamically from the PostgreSQL database instead of being hard-coded in the frontend.

Users can view available categories, select a category, and navigate to the appropriate quiz page using the category slug.

Category and quiz pages are protected so that only authenticated users can access quiz functionality.

Empty categories are handled appropriately to prevent users from starting a quiz that contains no questions.

### What Was Added

- Dynamic category retrieval using:

  - Category model

  - Django ORM

  - Count() aggregation

- Category listing functionality:

  - displays categories stored in the database

  - displays categories containing questions as selectable links

  - displays "No questions available" for empty categories

  - displays a message when no categories exist

- Category-specific quiz routing using:

  - category slugs

  - dynamic Django URL patterns

  - get_object_or_404()

- Authentication protection using:

  - @login_required on the categories view

  - @login_required on the category quiz view

- Empty category protection:

  - checks whether the selected category contains questions

  - redirects users back to the categories page when no questions exist

  - displays an informational message using Django's messaging framework

- Quiz template handling:

  - displays the selected category name

  - safely handles cases where no category context is provided

- Django Admin improvement:

  - corrected the Category plural name from "Categorys" to "Categories"

  - created and applied the required model options migration

### How It Works

1. Authenticated user selects `START QUIZ`

2. User is directed to `/categories/`

3. Django retrieves categories from the database

4. Each category is annotated with its number of questions

5. If a category contains questions:

   - it is displayed as a selectable link

   - its slug is used to generate the quiz URL

6. When the user selects a category:

   - Django retrieves the category using its slug

   - Django checks that the category contains questions

   - the selected category is passed to the quiz template

7. The category-specific quiz page is opened, for example:

   - `/quiz/driving-times/`

8. If a category contains no questions:

   - it is displayed as unavailable

   - direct URL access is prevented

   - the user is redirected back to the categories page with an informational message

9. Unauthenticated users attempting to access category or quiz pages are redirected to the login page

### Files Modified

- `quiz/views.py`

- `quiz/urls.py`

- `quiz/models.py`

- `quiz/templates/quiz/home.html`

- `quiz/templates/quiz/categories.html`

- `quiz/templates/quiz/quiz.html`

- `quiz/migrations/0002_alter_category_options.py`

### Testing

- Categories retrieved from PostgreSQL → success

- Available categories displayed → success

- Category containing questions → selectable

- Category selection → correct quiz URL opened

- Category slug → correct Category retrieved

- Empty category → displayed as unavailable

- Direct access to empty category → redirected to categories

- Empty category → informational message displayed

- Unauthenticated access to `/categories/` → redirected to login

- Unauthenticated access to category quiz URL → redirected to login

- Authenticated access to categories → success

- Category plural displayed as "Categories" in Django Admin → success

- `python manage.py check` → no issues

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

  ### US07 — Display Quiz Categories

- **Category URL error:**  
  A `NoReverseMatch` error occurred because the URL name in the template did not match the name defined in `urls.py`. This was fixed by using `category-quiz` consistently.

- **Empty category access:**  
  Categories without questions could still be accessed by entering their URL directly. A check using `category.questions.exists()` was added to redirect users back to the categories page.

- **Authentication protection:**  
  Code review identified that the new category views were accessible without authentication. `@login_required` was added to protect both category views.