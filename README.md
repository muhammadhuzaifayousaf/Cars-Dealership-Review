# Cars Dealership Review Platform

A full-stack web application developed as part of the **IBM Full Stack Software Developer Capstone Project**. The platform allows customers to explore car dealerships across the United States, view dealership details and customer reviews, and submit their own reviews after signing in.

## Project Overview

The goal of this project is to provide customers with a central platform for accessing dealership information and sharing their experiences, helping improve transparency and trust.

## Features

- **Dealership Directory:** Browse dealerships and view their details.
- **State-Based Filtering:** Find dealerships by selecting a U.S. state.
- **Dealership Reviews:** View customer reviews for individual dealerships.
- **User Authentication:** Register, log in, and log out.
- **Review Submission:** Authenticated users can submit reviews with purchase details and vehicle information.
- **Car Information:** Retrieve available car makes and models.
- **Sentiment Analysis:** Analyze review text to identify its sentiment.
- **Admin Management:** Use the Django administration interface to manage application data.
- **Responsive Interface:** Browse the application through a React-based frontend.
- **Cloud Deployment:** Deploy the application using Docker and IBM Cloud Code Engine.
- **Continuous Integration:** Run automated validation and frontend build checks with GitHub Actions.

## Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React.js, JavaScript, HTML, CSS, Bootstrap |
| Backend | Python, Django |
| API Integration | REST APIs, JSON, cURL |
| Database and Data Management | Django-supported data models and configured database |
| Build and Packaging | npm, Docker |
| Cloud Platform | IBM Cloud Code Engine |
| CI Workflow | GitHub Actions |
| AI Feature | Review sentiment analysis |

## Live Application

**Deployment URL:**  
https://cars-dealership-capstone.2fvlkql47akz.us-south.codeengine.appdomain.cloud/

## Main API Endpoints

The application provides endpoints for dealership information, reviews, authentication, car data, and sentiment analysis.

| Endpoint | Purpose |
|---|---|
| `/djangoapp/get_dealers` | Retrieve all dealerships |
| `/djangoapp/get_dealers/<state>` | Retrieve dealerships for a state |
| `/djangoapp/dealer/<dealer_id>` | Retrieve dealership details |
| `/djangoapp/reviews/dealer/<dealer_id>` | Retrieve reviews for a dealership |
| `/djangoapp/add_review` | Submit a dealership review |
| `/djangoapp/get_cars` | Retrieve car information |
| `/djangoapp/analyze_review` | Analyze review sentiment |
| `/djangoapp/login` | Authenticate a user |
| `/djangoapp/logout` | Log out a user |

Replace path parameters such as `<state>` and `<dealer_id>` with the required values when testing the endpoints.

## Run Locally

### Prerequisites

- Python 3.11 or a compatible Python version
- Node.js and npm
- Git

### Backend

```bash
git clone https://github.com/muhammadhuzaifayousaf/ibm-fullstack-developer-capstone.git
cd ibm-fullstack-developer-capstone/server

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

Open another terminal:

```
cd ibm-fullstack-developer-capstone/server/frontend

npm install
npm start
```

The frontend may require the Django backend to be running for API requests to work. Deployment-specific configuration may also be needed when running the application locally.

## Deployment and Continuous Integration

The application is containerized with Docker and deployed to IBM Cloud Code Engine. A GitHub Actions workflow is defined in `.github/workflows/ci.yml` to validate the Django configuration and build the React frontend.

GitHub repository: [https://github.com/muhammadhuzaifayousaf/ibm-fullstack-developer-capstone](https://github.com/muhammadhuzaifayousaf/ibm-fullstack-developer-capstone)

GitHub Actions: [https://github.com/muhammadhuzaifayousaf/ibm-fullstack-developer-capstone/actions](https://github.com/muhammadhuzaifayousaf/ibm-fullstack-developer-capstone/actions)

## Learning Outcomes

This project demonstrates practical experience with full-stack web development, frontend and backend integration, REST API testing, authentication, database-backed applications, automated build validation, containerization, cloud deployment, and sentiment analysis.

## Author

Muhammad Huzaifa Yousaf

GitHub: [https://github.com/muhammadhuzaifayousaf](https://github.com/muhammadhuzaifayousaf)

Portfolio: [https://muhammadhuzaifayousaf.vercel.app/](https://muhammadhuzaifayousaf.vercel.app/)

Developed as part of the IBM Full Stack Software Developer Capstone Project. 
