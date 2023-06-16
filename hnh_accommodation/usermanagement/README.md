# User Management API Endpoints

## User Registration Endpoint:

URL: `/api/register/`
HTTP Method: `POST`
Description: This endpoint is used to register a new user.
Request Body: JSON object containing user registration data (name, email, password).
Response: JSON object with a success message or an error message if registration fails.

## User Login Endpoint:

URL: `/api/login/`
HTTP Method: `POST`
Description: This endpoint is used to authenticate a user and generate an authentication token.
Request Body: JSON object containing user login credentials (username, password).
Response: JSON object with an authentication token if login is successful or an error message if login fails.

## User Profile Endpoint:

URL: `/api/users/{user_id}/`
HTTP Method: `GET`, `PUT`, `PATCH`
Description: This endpoint is used to retrieve, update, or delete a user's profile.
Request Body (for update): JSON object containing updated user profile data.
Response: JSON object with user profile data or an error message.
