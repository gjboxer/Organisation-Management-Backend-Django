# Django Organization Management App

This Django app is designed to manage organizations, memberships, invitations, and tasks. It provides a set of APIs to create, join, and manage organizations, invite members, and assign tasks to users within those organizations.

## Features

1. **Organization Management**: Create, list, update, and delete organizations with details like name and description.

2. **User Membership**: Users can join organizations. You can check if a user is already a member of an organization to prevent duplicates.

3. **Invitations**: Users can send and receive invitations to join organizations. Invitations can be accepted or rejected.

4. **View Task Assignment**: Users can see the task assigned to them in an organisation

## API Endpoints

### Organization Management

#### List Organizations
- `GET /organizations/`: List all organizations.

#### Retrieve Organization
- `GET /organizations/<int:pk>/`: Retrieve details of a specific organization.

#### Create Organization
- `POST /organizations/`: Create a new organization.

#### Update Organization
- `PUT /organizations/<int:pk>/`: Update an organization.

#### Delete Organization
- `DELETE /organizations/<int:pk>/`: Delete an organization.

### User Organization Management

#### List Current User's Organizations
- `GET /current-user-organization/`: List organizations that the current user is a member of.

#### Join an Organization
- `POST /join-organization/`: Join an organization.

### Invitations

#### List User Invitations
- `GET /user-invitations/`: List invitations received by the current user.

#### Send an Invitation
- `POST /invitations/`: Send an invitation to another user to join an organization.

#### Accept or Reject Invitation
- `PATCH /invitations/<int:pk>/accept-reject/`: Accept or reject an invitation.

### Task Assignment

#### List User Tasks
- `GET /tasks/`: List tasks assigned to the current user.

## Usage

1. **Installation**

   - Clone this repository from GitHub.
   - Install the required packages using `pip install -r requirements.txt`.
   - Migrate the database using `python manage.py migrate`.

2. **API Authentication**

   - The API endpoints are protected, and users need to be authenticated.
   - You can create a superuser account using `python manage.py createsuperuser` for admin access.

3. **Admin Panel**

   - The Django admin panel (`/admin/`) can be used for managing organizations, users, tasks, and invitations.

4. **Running the App**

   - To run the app, use the following command:
     ```
     python manage.py runserver
     ```

5. **Accessing the App**

   - Once the app is running, you can access it through a web browser at `http://127.0.0.1:8000/`.
