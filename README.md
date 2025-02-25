# Airport API

## Features
- JWT Authentication 
- Admin panel
- Documentation is located at /api/v1/doc/swagger/
- Managing orders and tickets for flights
- Adding airplanes with images, airports, routes, crew, flights (available for admin users)
- Filtering airplanes, airports, crew, flights

## How to use

### From GitHub

**For Windows:**
```shell
git clone https://github.com/dottfmar/airport-api.git
cd airport-api
python -m venv venv
venv\Scripts\activate
docker-compose up --build
```

**For MacOS:**
```shell
git clone https://github.com/dottfmar/airport-api.git
cd airport-api
python3 -m venv venv
source venv/bin/activate
docker-compose up --build
```

You can open project via IDE and configure .env file using .env.sample as example
### Image on DockerHub

```shell
docker login
docker pull dottfmar/airport_service_api:latest
```

## Credentials of admin user

Email: admin@admin.com

Password: 1234


### Extra
Obtain access token via http://127.0.0.1:8000/user/token/

#### About calculating of distance between two airports

I used for that Haversine formula. More details about it here: https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/
