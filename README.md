# rotaguard-tool

## Overview


Open source tool to allow timesheet management. Built in compliance with UK Working Time Regulations 1998.


This tool comes about as there appears to be a need for a tool which allows managers/owners employing shift workers to fail to comply with the UK WTR rules. Most times, this is done through lack of knowledge, despite this legislation having been in place than many managers have been alive.

## The rules

Summarised, they are:

Maximum working hours

48 hours per week on average (unless the worker has “opted out”).

Rest breaks during the day

At least 20 minutes if the shift is longer than 6 hours.

Daily rest

At least 11 consecutive hours rest in each 24-hour period.

Weekly rest

At least 24 hours without work each week, or 48 hours every two weeks.

Night work limits

Special protections for night workers (generally capped at 8 hours in any 24-hour period, on average).

# The tool aims to provide

1. An easy to use interface to allow shift management.
2. Team management
3. Role management (i.e an indivuals job title)
4. Individual availability
5. Daily/weekly time tracking
6. Parsing and compliance-verification of rota's provided in either JSON or CSV format (format TBC)

# The tool does not aim to provide

1. Approval/disapproval of annual leave requests. That is for people, not computers.
2. Holiday time accrual/use.
3. Payroll management

# Project Breakdown

## User Stories

### Epic: Shift Management

*   **As a manager, I want to create, view, update, and delete shifts for my team so that I can schedule work effectively.**
*   **As a manager, I want to assign shifts to specific team members.**
*   **As a team member, I want to view my upcoming shifts so I know when I am scheduled to work.**
*   **As a manager, I want to import a rota from a JSON or CSV file to quickly populate the schedule.**
*   **As a manager, I want the system to validate the imported rota against UK Working Time Regulations to ensure compliance.**

### Epic: Team Management

*   **As a manager, I want to add new team members to the system.**
*   **As a manager, I want to view a list of all team members.**
*   **As a manager, I want to edit team member details (e.g., name, contact info).**
*   **As a manager, I want to remove team members who no longer work for the company.**

### Epic: Role Management

*   **As a manager, I want to define different job roles within the organization (e.g., "Cashier", "Chef").**
*   **As a manager, I want to assign roles to my team members.**

### Epic: Availability Management

*   **As a team member, I want to set my availability (i.e., days and times I can or cannot work) so my manager can schedule me appropriately.**
*   **As a manager, I want to view my team members' availability when creating shifts.**

### Epic: Time Tracking

*   **As a team member, I want to clock in and clock out for my shifts to record my actual work hours.**
*   **As a manager, I want to view daily and weekly time tracking reports for my team.**
*   **As a manager, I want to be alerted when a team member is approaching or has exceeded the 48-hour average weekly work limit.**
*   **As a manager, I want the system to flag shifts that violate rest break, daily rest, or weekly rest rules.**

## Framework Recommendations

Here are three recommendations for building this application, covering the backend, database, and frontend.

1.  **The "Modern JavaScript" Stack**
    *   **Backend: Node.js with Express.js or a framework like NestJS.**
        *   *Why:* Node.js is excellent for I/O-heavy applications like this one will be (lots of database reads and writes). Express is a minimal and flexible Node.js web application framework that provides a robust set of features for web and mobile applications. NestJS is a more opinionated, TypeScript-based framework that provides a more structured architecture, which can be beneficial for larger, more complex applications.
    *   **Database: PostgreSQL**
        *   *Why:* PostgreSQL is a powerful, open-source object-relational database system with over 30 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance. It's great for handling the relational data we'll have (users, shifts, roles).
    *   **Frontend: React or Vue.js**
        *   *Why:* Both are popular, component-based frameworks that make it easy to build interactive user interfaces. React has a massive ecosystem and community support. Vue.js is often considered easier to learn and has excellent documentation.

2.  **The "Pythonic" Stack**
    *   **Backend: Python with Django or Flask.**
        *   *Why:* Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. It includes an ORM, which simplifies database interactions. Flask is a micro-framework that is more lightweight and flexible, allowing you to choose your own libraries and tools.
    *   **Database: PostgreSQL or MySQL.**
        *   *Why:* Both are excellent, reliable, and widely used open-source relational databases that work well with Python backends.
    *   **Frontend: HTMX or a simple JavaScript framework like Alpine.js.**
        *   *Why:* If you want to keep the frontend simple and render most of the HTML on the server, HTMX allows you to access modern browser features directly from HTML, rather than using javascript. This can lead to a simpler and more maintainable frontend.

3.  **The "All-in-One" Solution**
    *   **Backend/Frontend: Next.js (with React)**
        *   *Why:* Next.js is a React framework that provides a hybrid of static and server-rendering. It can handle both the frontend and backend (with API routes), simplifying the development process and deployment. It has a great developer experience and is well-suited for this type of application.
    *   **Database: SQLite or PostgreSQL.**
        *   *Why:* For a smaller application, SQLite could be sufficient and is very easy to set up (it's just a file). For a more robust and scalable solution, PostgreSQL is a better choice. Next.js works well with both.

---

## Getting Started

### Initial Setup

This project is fully containerized using Docker. To get started, you will need Docker and Docker Compose installed.

1.  **Build and Run the Containers:**
    This command will build the necessary Docker images and start the Flask (`web`) and PostgreSQL (`db`) services. The `-d` flag runs them in detached mode.

    ```bash
    docker-compose up --build -d
    ```

2.  **Set Up the Database:**
    With the containers running, execute the following commands to initialize the database, create the initial migration, and apply it.

    ```bash
    # Initialize the migrations folder (only needs to be run once)
    docker-compose exec web flask db init

    # Create the migration script based on your models
    docker-compose exec web flask db migrate -m "Initial migration."

    # Apply the migration to the database
    docker-compose exec web flask db upgrade
    ```

3.  **Create the First Admin User:**
    Use the following `curl` command to register the first manager/admin user.

    ```bash
    curl -X POST -H "Content-Type: application/json" \
    -d '{"email":"manager@example.com", "password":"securepassword123", "name":"Admin Manager"}' \
    http://localhost:5000/api/auth/register
    ```

---

## Debugging with vsdebug.py (debugpy helper)

To simplify starting Python debugging sessions in your container, you can use a helper script (e.g., `vsdebug.py` or `vsdebug.sh`).

### 1. Create the script locally

Create a file named `vsdebug.py` or `vsdebug.sh` with the following contents:

```bash
#!/bin/bash
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client "$@"
```

### 2. Make the script executable

```bash
chmod +x vsdebug.sh
```

### 3. Add the script to your Docker image

In your `Dockerfile`, add:

```dockerfile
COPY vsdebug.sh /usr/bin/vsdebug
RUN chmod +x /usr/bin/vsdebug
```

This will make `vsdebug` available anywhere in your running container.

### 4. Usage in the container

After building and starting your container, you can run:

```bash
docker compose exec web vsdebug pytest
```
Or for any Python module
```bash
docker compose exec web vsdebug myscript.py
```
or

```bash
docker compose exec web vsdebug -m pytest tests/path/to/test_thing.py
```

This will start your Python process with debugpy, listening for VS Code to attach on port 5678.

---

## API: Role Management

### Create a Role
`POST /api/roles/`

Request body:
```json
{
  "name": "Cashier"
}
```
Response:
- **201 Created**: Returns the created role object.

### List Roles
`GET /api/roles/`

Response:
- **200 OK**: Returns a list of all roles.

### Get Role by ID
`GET /api/roles/<role_id>`

Response:
- **200 OK**: Returns the role object.
- **404 Not Found**: If the role does not exist.

---

## API: Assign Roles to a User

### Endpoint

`PUT /api/users/<user_id>/roles`

Assigns a list of roles to a user. Only accessible to managers (permission logic should be enforced in production).

#### Request Body
```json
{
  "role_names": ["Cashier", "Chef"]
}
```

#### Success Response
- **Status:** 200 OK
- **Body:**
```json
{
  "message": "Roles updated successfully"
}
```

#### Error Responses
- **400 Bad Request**: One or more roles not found
- **404 Not Found**: User not found

#### Example Usage
```bash
curl -X PUT -H "Content-Type: application/json" \
  -d '{"role_names": ["Cashier", "Chef"]}' \
  http://localhost:5000/api/users/<user_id>/roles
```

This endpoint allows a manager to assign or update the roles for any user. The user’s roles will be replaced with the provided list.

---

## Note: Permissions

Role-based permissions (e.g., assigning specific permissions to roles) are not yet implemented. This is planned for a future sprint and will allow fine-grained access control for different user types.

