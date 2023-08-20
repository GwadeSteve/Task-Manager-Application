# Task Manager Web App

## Description

The Task Manager Web App is a web application built using Django and Django Rest Framework. It allows users to manage their tasks by providing a user-friendly interface for creating, updating, and deleting tasks. The app also offers a RESTful API for programmatic access to task data.

## Features

- User registration and authentication.
- Task creation, updating, and deletion.
- RESTful API for task CRUD operations.
- Responsive and user-friendly interface.

## Technologies Used

- Django
- Django Rest Framework
- HTML/CSS/JS
- PostgreSQL

## Getting Started

1. Clone this repository.
2. Set up your Python virtual environment.
3. Install project dependencies: `pip install -r requirements.txt`
4. Configure your database settings in `settings.py`.
5. Run migrations: `python manage.py migrate`
6. Start the development server: `python manage.py runserver`
7. Access the app at `http://127.0.0.1:8000`

## Screenshots

...

## API Doumentation

Refer to the API documentation.md file in this repo

## App Usage

1. **Registration and Login:**
   - Open the app in your web browser.
   - Click on the "Sign Up" link to create a new account.
   - Fill in your email, username, and password, then click "Register."
   - Once registered, log in using your credentials.

2. **Dashboard and Task List:**
   - After logging in, you'll be directed to your dashboard.
   - The dashboard displays a list of your tasks, along with their titles, descriptions, and completion status.

3. **Create a New Task:**
   - To create a new task, click the "Create New Task" button.
   - Enter a title and description for the task, then click "Submit."
   - The new task will be added to your task list.

4. **Update a Task:**
   - To update an existing task, click on the task in the list.
   - Edit the title, description, or other details as needed.
   - Click "Save" to update the task.

5. **Complete a Task:**
   - Mark a task as completed by clicking the checkbox next to it.
   - The task's completion status will be updated, and you'll see a visual indicator.

6. **Delete a Task:**
   - To delete a task, click the "Delete" button next to the task.
   - Confirm the deletion, and the task will be removed from your list.

7. **Logout:**
   - When you're done, click on the "Log Out" link to log out of your account.
   - Your session will be terminated, and you'll need to log in again to access your tasks.


## License

This project is licensed under the [MIT License](LICENSE).


