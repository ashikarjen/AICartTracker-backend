# AI Cart Tracker Backend

## Overview
The AI Cart Tracker Backend is a learning-based demo project developed to explore the integration of web scraping, Natural Language Processing (NLP), and backend technologies. It allows users to track products from e-commerce websites like Daraz by interacting with the system using natural language. This project is intended solely for educational purposes and not for commercial use.

## Features
1. **Natural Language Input:** Users can provide product URLs along with instructions in natural language (e.g., "Track this product").
2. **NLP Integration:** The system uses NLP to extract product URLs and understand user intent from the input text.
3. **Product Tracking:** Automatically scrapes and tracks product details, such as price, title, and ratings, over time.
4. **Asynchronous Processing:** Handles scraping tasks asynchronously to improve performance and user experience.
5. **Dockerized Deployment:** Fully containerized using Docker, making it easy to deploy and run on various environments.
6. **CI/CD Pipeline:** Uses GitHub Actions for continuous integration and deployment to ensure smooth and automated updates.

## Technology Stack
1. **Backend:** Django
2. **NLP:** spaCy for processing and extracting URLs and intents from user input.
3. **Task Queue:** Celery for handling asynchronous tasks like scraping.
4. **Message Broker:** Redis to manage task queues.
5. **Database:** PostgreSQL for storing product and user data.
6. **Containerization:** Docker and Docker Compose for packaging and deployment.
7. **Web Server:** Gunicorn to serve the Django application.
8. **CI/CD:** GitHub Actions to automate the build, test, and deployment processes.

## How It Works
1. **User Input:** Users provide text input that includes product URLs and commands (e.g., "Please track this product: [URL]").
2. **NLP Processing:** The NLP module extracts the URL and determines the user's intent (e.g., tracking the product).
3. **Product Scraping:** If the input command matches tracking, the system starts scraping the product's details from the URL.
4. **Data Storage:** Scraped data is stored in a PostgreSQL database, allowing the system to track changes over time.
5. **Asynchronous Tasks:** Long-running scraping tasks are managed by Celery workers and queued using Redis, ensuring the system remains responsive.
6. **API Responses:** The application provides API endpoints that return the status and results of the scraping tasks.

## Deployment
The project is fully containerized using Docker, allowing for easy setup and deployment. The application, database, and other services are defined in a docker-compose.yml file, enabling all components to run seamlessly in isolated containers.

## CI/CD Pipeline
A GitHub Actions workflow automates the continuous integration and deployment process. The pipeline builds the Docker image, runs tests, and pushes the image to Docker Hub whenever changes are pushed to the main branch.

## Future Enhancements
1. **Advanced NLP:** Implement more sophisticated NLP models for improved intent recognition and custom entity extraction.
2. **User Authentication:** Add user accounts and authentication for personalized tracking and notifications.
3. **Frontend Integration:** Develop a user-friendly frontend to interact with the backend services visually.
4. **Scalability Improvements:** Optimize the application to handle more users and larger volumes of data.

## Conclusion
The AI Cart Tracker Backend is a learning-focused demonstration of integrating modern web technologies and NLP for product tracking. This project showcases how backend services can interact with real-world data in an educational context. Please note that this project is not intended for commercial use and serves solely as an educational tool for learning and experimentation.
