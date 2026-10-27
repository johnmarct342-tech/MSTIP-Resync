# MSTIP RoomSync
A web-based room reservation and scheduling system for Makati Science Technological Institute of the Philippines (MSTIP).

## Features
- User Authentication (Login/Logout)
- Real-time Room Availability viewing
- Automated Conflict Checking (Prevents Double Bookings)
- Admin Approval Dashboard
- Live JavaScript warnings for scheduled classes

## Technologies Used
- **Backend:** Python (Django)
- **Database:** SQLite
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript

## How to Run Locally
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`
