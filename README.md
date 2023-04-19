# Project info

## Make a RESTful web API for a restaurant review project

### Features:
- User authentication & Authorization with two roles (Restaurant Owner & Regular user)
- The ability to CRUD is limited to restaurant owners
- Ability for visitors to create and read reviews for a specific restaurant
- A review should have the following at minimum
- Filtering restaurants by average rating
- All API endpoints should be paginated

# Project run basics
To run the project:
- Install dependencies with pipenv
- Make sure you have CONFIGURATION_SETUP environment variable 
    - CONFIGURATION_SETUP=config.DevelopmentConfig
    - CONFIGURATION_SETUP=config.ProductionConfig
- Run flask server on app.py
- Enter http://127.0.0.1:5000/api/doc
  - Here is the documentation for the api routes