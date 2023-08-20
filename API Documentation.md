## API Documentation

The Task Manager Web App offers a RESTful API for programmatic access to task data. You can use these API endpoints to perform CRUD (Create, Read, Update, Delete) operations on tasks.

### Base URL

The base URL for accessing the API endpoints is: ...


### Endpoints

#### Get All Tasks
- **URL:** `/api/tasks/`
- **Method:** GET
- **Description:** Get a list of all tasks.
- **Example Request:** `GET /api/tasks/`
- **Example Response:**
```[
  {
    "id": 1,
    "title": "Complete Project Proposal",
    "description": "Write and submit the project proposal by Friday.",
    "completed": false,
    "created_at": "2023-08-17T12:00:00Z"
  },
  {
    "id": 2,
    "title": "Prepare Presentation Slides",
    "description": "Create slides for the project presentation.",
    "completed": false,
    "created_at": "2023-08-18T09:30:00Z"
  },
  // ...
] ```

#### Get Task by ID
- **URL:** `/api/tasks/{task_id}/`
- **Method:** GET
- **Description:** Get details of a specific task by its ID.
- **Example Request:** `GET /api/tasks/1/`
-**Example Response:**
```{
  "id": 1,
  "title": "Complete Project Proposal",
  "description": "Write and submit the project proposal by Friday.",
  "completed": false,
  "created_at": "2023-08-17T12:00:00Z"
}```

#### Create Task
- **URL:** `/api/tasks/`
- **Method:** POST
- **Description:** Create a new task.
- **Example Request:**
  ```POST /api/tasks/
     Content-Type: application/json
     
     {
       "title": "Buy Groceries",
       "description": "Purchase items for dinner tonight."
     }
```
- **Example Response:**
```{
  "id": 3,
  "title": "Buy Groceries",
  "description": "Purchase items for dinner tonight.",
  "completed": false,
  "created_at": "2023-08-19T15:20:00Z"
}```

#### Update Task
- **URL:** `/api/tasks/{task_id}/`
- **Method:** PUT
- **Description:** Update details of a specific task.
- **Example Request:**
```PUT /api/tasks/2/
Content-Type: application/json

{
  "title": "Prepare Presentation Slides",
  "description": "Create slides for the project presentation. Include graphs and images."
}```
- **Example Response:**
```{
  "id": 2,
  "title": "Prepare Presentation Slides",
  "description": "Create slides for the project presentation. Include graphs and images.",
  "completed": false,
  "created_at": "2023-08-18T09:30:00Z"
}```
