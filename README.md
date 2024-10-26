ToDo API Project
Overview
The ToDo API is a RESTful API built using Django and Django REST Framework (DRF) to manage ToDo tasks for authenticated users. This API allows users to create, retrieve, update, and delete ToDo items, while also providing filtering, sorting, and validation functionalities. It is secured using JWT-based authentication and includes user-specific task management, ensuring that users can only access and manipulate their own data.

Key Features
User Authentication:
Uses JWT (JSON Web Tokens) for secure user authentication.
Ensures that only authenticated users can access the API endpoints.
CRUD Operations:
Create, retrieve, update, and delete ToDo tasks.
Allows users to manage their own ToDo list.
Filtering and Sorting:
Allows filtering of ToDo items based on status and due_date.
Supports ordering tasks by due_date for easier task management.
Validation:
Ensures that the due_date is not earlier than the created_at date.
Prevents invalid data entry, maintaining the integrity of ToDo items.
Swagger Documentation:
Interactive API documentation is available via Swagger at http://127.0.0.1:8000/swagger/.
API Endpoints
1. Swagger API Documentation
URL: Swagger UI
Description: Provides a user-friendly interface to explore the available API endpoints and test them directly from the browser.
2. List All ToDo Items for the User
URL: View All Tasks
Description: Lists all ToDo items for the authenticated user.
Filtering: Supports filtering by status and due_date.
Example: GET /api/all?status=pending&due_date=2024-11-01
Ordering: Supports ordering by due_date.
Example: GET /api/all?ordering=due_date
Authentication: JWT required.
3. Create a ToDo Item
URL: Create a Task
Description: Allows the creation of a new ToDo item for the authenticated user.
Request Body:
json
Copy code
{
  "title": "Buy groceries",
  "description": "Milk, Bread, Eggs",
  "due_date": "2024-11-01"
}
Response: Returns the created ToDo item.
Authentication: JWT required.
4. Retrieve a Specific ToDo Item
URL: GET http://127.0.0.1:8000/api/<id>/ (where <id> is the ID of the task)
Description: Retrieves details of a specific ToDo item by its ID.
Example: Retrieve a Task for ID = 1.
Response:
json
Copy code
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, Bread, Eggs",
  "created_at": "2024-10-27",
  "due_date": "2024-11-01",
  "status": "pending"
}
Authentication: JWT required.
5. Update a ToDo Item
URL: PUT http://127.0.0.1:8000/api/<id>/ (where <id> is the ID of the task)
Description: Updates the details of a specific ToDo item.
Example: Update the task with ID 1.
Request Body:
json
Copy code
{
  "title": "Buy groceries and fruits",
  "due_date": "2024-11-02",
  "status": "completed"
}
Validation: Ensures created_at is not later than due_date.
Authentication: JWT required.
6. Delete a ToDo Item
URL: DELETE http://127.0.0.1:8000/api/<id>/ (where <id> is the ID of the task)
Description: Deletes a specific ToDo item.
Response: Status 204 No Content on successful deletion.
Authentication: JWT required.
7. User Authentication Endpoints
Login: Login User
Logout: Logout User
Register: Register New User
User Info: View User Information
Description: Allows users to register, login, and manage their session via JWT tokens. The user info endpoint provides details about the authenticated user.
Models
ToDo Model
Fields:
title: The title of the ToDo item.
description: A brief description of the task.
created_at: The timestamp when the task was created (auto-generated).
due_date: The date by which the task should be completed.
status: The current status of the task (e.g., "pending", "completed").
user: A foreign key that links each ToDo item to a specific user.
Serializers
ToDoListSerializer
Converts ToDo model instances into JSON format and validates input data.
Ensures that due_date is not earlier than created_at using custom validation logic.
Supports fields: id, title, description, created_at, due_date, status.
Filters and Sorting
Filtering
Uses DjangoFilterBackend to enable filtering by status and due_date.
Supports filtering tasks for a specific date.
Sorting
Uses OrderingFilter to allow sorting of ToDo items by due_date in ascending or descending order.
Authentication
JWT Authentication
Uses JWTAuthenticationFromCookie to handle JWT tokens from cookies for secure access.
Ensures that users can only access their own ToDo items.
