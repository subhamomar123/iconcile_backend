# Hotel Management API

## Overview

This API provides comprehensive functionalities for managing hotel data, user interactions, and reservations. It supports operations such as CRUD for hotels, user visit management, booking details, and draft handling. Additionally, it offers recommendations based on user activity and hotel ratings.

## Models

### `HotelDetails`
- **Table Name**: `hotel_details`
- **Description**: Stores details about hotels.
- **Columns**:
  - `id` (INT, Primary Key, Auto Increment): Unique identifier for each hotel.
  - `name` (VARCHAR(255), NOT NULL): Name of the hotel.
  - `amenities` (TEXT): List of amenities provided by the hotel.
  - `description` (TEXT): Description of the hotel.
  - `location` (VARCHAR(255)): Location of the hotel.
  - `rating` (DECIMAL(3, 2)): Rating of the hotel (0.00 to 5.00).

### `ReservationsTracking`
- **Table Name**: `reservations_tracking`
- **Description**: Tracks visit and booking counts for each hotel.
- **Columns**:
  - `hotel_id` (INT, Primary Key, Foreign Key): Reference to the hotel.
  - `visits_count` (INT, Default: 0): Number of times the hotel has been visited.
  - `bookings_count` (INT, Default: 0): Number of bookings made for the hotel.

### `DraftDetails`
- **Table Name**: `draft_details`
- **Description**: Stores draft information for users.
- **Columns**:
  - `user_id` (INT, Primary Key): User identifier.
  - `hotel_id` (INT, Primary Key, Foreign Key): Hotel identifier.
  - `draft` (TEXT): Draft content for the user.

### `UserVisitDetails`
- **Table Name**: `user_visit_details`
- **Description**: Records each visit made by a user to a hotel.
- **Columns**:
  - `id` (INT, Primary Key, Auto Increment): Unique identifier for each visit record.
  - `user_id` (INT, Foreign Key): User identifier.
  - `hotel_id` (INT, Foreign Key): Hotel identifier.
  - `time` (TIME): Time of the visit.
  - `date` (DATE): Date of the visit.

### `BookingDetails`
- **Table Name**: `booking_details`
- **Description**: Stores booking details for users.
- **Columns**:
  - `booking_id` (INT, Primary Key, Auto Increment): Unique identifier for each booking.
  - `user_id` (INT, Foreign Key): User identifier.
  - `hotel_id` (INT, Foreign Key): Hotel identifier.
  - `time` (TIME): Time of the booking.
  - `date` (DATE): Date of the booking.

### `User`
- **Table Name**: `users`
- **Description**: Stores user credentials.
- **Columns**:
  - `user_id` (INT, Primary Key, Auto Increment): Unique identifier for each user.
  - `username` (VARCHAR(255), NOT NULL): Username of the user.
  - `password` (VARCHAR(255), NOT NULL): Encrypted password of the user.

## API Endpoints

### `/hotel/<int:id>`
- **Method**: `GET`
- **Description**: Retrieve details of a hotel by its ID and increment its visit count. Optionally records a visit for a user if `user_id` is provided.
- **Query Parameters**:
  - `user_id` (Optional, INT): User ID to record the visit.
- **Responses**:
  - `200 OK`: Returns hotel details and updated visit count.
  - `404 Not Found`: Hotel not found.
- **Logic**:
  - Retrieves the hotel information.
  - Increments the visit count for the hotel.
  - Records a user visit if `user_id` is provided (defaults to `-1` if not).

### `/hotel/checkout`
- **Method**: `POST`
- **Description**: Book a hotel for a user and increment the booking count.
- **Request Body**:
  - `user_id` (INT): User ID (Mandatory).
  - `hotel_id` (INT): Hotel ID (Mandatory).
- **Responses**:
  - `201 Created`: Booking successful, returns booking ID.
  - `400 Bad Request`: Missing `user_id` or `hotel_id`.
  - `404 Not Found`: Hotel or user not found.
- **Logic**:
  - Creates a booking entry.
  - Increments the booking count for the hotel.

### `/hotel/<int:id>/draft`
- **Method**: `POST`
- **Description**: Save or update a draft for a user and hotel.
- **Request Body**:
  - `user_id` (INT): User ID (Mandatory).
  - `draft` (STRING): Draft content (Mandatory).
- **Responses**:
  - `200 OK`: Draft saved or updated successfully.
  - `400 Bad Request`: Missing `user_id` or `draft`.
- **Logic**:
  - Updates the draft if it exists, otherwise creates a new draft.

- **Method**: `GET`
- **Description**: Retrieve the draft for a user and hotel.
- **Query Parameters**:
  - `user_id` (INT): User ID (Mandatory).
- **Responses**:
  - `200 OK`: Returns draft content.
  - `404 Not Found`: Draft not found.
- **Logic**:
  - Retrieves the draft associated with the user and hotel.

### `/suggest`
- **Method**: `GET`
- **Description**: Suggest hotels based on user visit history or top ratings.
- **Query Parameters**:
  - `user_id` (Optional, INT): User ID.
- **Responses**:
  - `200 OK`: Returns a list of suggested hotels.
- **Logic**:
  - If `user_id` is not provided, return the top 5 hotels with the highest ratings.
  - If `user_id` is provided, check the user's last visit and return the top 5 hotels based on the last visit's location. If no visit history is found, return top 5 rated hotels.

### `/hotel/bookings`
- **Method**: `GET`
- **Description**: Retrieve total visits, completed bookings, and draft bookings for a hotel.
- **Query Parameters**:
  - `hotel_id` (INT): Hotel ID.
- **Responses**:
  - `200 OK`: Returns visits, completed bookings, and draft bookings for the specified hotel.
- **Logic**:
  - Fetches and returns aggregated data about the hotel's visits, bookings, and drafts.

## Swagger Documentation

Swagger documentation provides interactive API documentation. Each endpoint includes:
- **Summary**: Brief description of the endpoint’s functionality.
- **Parameters**: Query parameters and request body details.
- **Responses**: Possible responses with their status codes and content types.
- **Examples**: Example request and response payloads.

## Setup and Usage

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the Database**: Set up the MySQL database and update the connection string in the Flask app.

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access Swagger UI**: Open `http://localhost:5000/swagger` in your browser to interact with the API.

