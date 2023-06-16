# HNH BACKEND
A Django based backend for the hnh accommodation app.
The frontend is at [hnh-accommodation](https://github.com/esmond-adjei/hnh-accommodation)

---
# Hostel Accommodation App

This is a Django-based web application for managing hostel accommodations.

## Getting Started

Follow the steps below to set up and run the project locally.

### Prerequisites

- Python 3.10 or higher
- Django 4.1 or higher

### Installation

1. Clone the repository:
```
git clone https://github.com/esmond-adjei/hnh-backend.git
```

2. Navigate to the project directory:
```
cd hnh_accommodation
```

3. Create a virtual environment (optional by recommended):
```
python3 -m venv <venv name>
```

4. Activate the virtual environment:
- For Linux or macOS:
  ```
  source venv/bin/activate
  ```
- For Windows:
  ```
  venv\Scripts\activate
  ```

5. Install the Python dependencies:
```
pip3 install -r requirements.txt
```


### Configuration

1. Rename the `hnh_accommodation/.env.example` file to `.env`.

2. Edit the `.env` file and update the configuration variables as needed.

### Database Setup

1. Apply the database migrations:
```
python manage.py migrate
```

### Running the App

1. Start the Django development server:
```
python manage.py runserver
```

---

# Contributing

If you would like to contribute to this project, please follow these guidelines:

1. Fork the repository and create your branch.
2. Make your changes and commit them with descriptive messages.
3. Push your changes to your forked repository.
4. Create a pull request to the main repository.
