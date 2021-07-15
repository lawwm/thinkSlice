# ThinkSlice
![Proper banner](https://user-images.githubusercontent.com/41231584/125463162-bc2d16c6-be40-40f6-913d-b332e35f610f.png)
### Bringing students and educators together with the help of video! 
Traditional qualifiers such as logistics and qualifications are not sufficient to represent teaching quality. Using the **thin-slicing effect**, students can find the right teachers for them by watching videos of teachers teaching their specialty.

**For tutors:** 
1. Upload short educational videos to showcase your teaching ability.
2. Provide more information about yourself on your profile.
3. Potential students contact you to setup a lesson.

**For students:** 
1. Browse through a catalog of videos to find a teacher that fits your vibe.
2. Check out their profile and reviews.
3. Chat with your potential educator to setup a lesson.

&nbsp;
## Orbital
This project was produced under NUS Orbital (CP2106).

**Level of Achievement**:  Apollo 11

**Web Application**:  https://thinkslice.vercel.app/

**Milestone 3**:  https://docs.google.com/document/d/12ZJZre344KpwpnLlnluU_pgUe5PbZxOR7vvVEONswkI/edit

**Frontend Github**:  https://github.com/lawwm/thinkSlice-frontend

&nbsp;
## Prerequisites
- Yarn
- Python 3
- pipenv

&nbsp;
## Installation Guide
Install dependencies as follows.

&nbsp;
### Backend Django Guide
- Installing dependencies
```
cd appmanager
pipenv install
```
- Starting the server
```
pipenv shell
cd appmanager
python manage.py runserver
```
- Access the server on "http://localhost:8000"
- Closing the server 
```
exit
```
&nbsp;
### Frontend React Installation
- Installing dependencies
```
cd frontend
yarn install
```
- Starting the server
```
yarn start
```
- Access the server on "http://localhost:3000"

&nbsp;
## Tests Runner Guide
For the frontend, Jest is used for unit testing while Cypress is used for End-to-End tests. Jest files are found within "__tests__" files inside store folder, while cypress files are stored within "cypress/integration/thinkslice" directory. Mock service worker is used for mocking API calls for uniting testing (Jest).

For the backend, python is used for unit testing.

&nbsp;
### Jest
- Start Jest Runner
```
yarn test
```
- Start Jest code coverage
```
yarn run test -- --coverage --watchAll=false
```
&nbsp;
### Cypress
- Start cypress runner
```
yarn run cypress open
```
&nbsp;
### Python Testing
- Start Python Code Coverage
```
coverage run manage.py test .  -v 2
coverage html
```
Note: You need a local PostgreSQL server for testing.

&nbsp;
## Deployment Guide
We used Vercel for frontend development and Heroku for backend development.

&nbsp;
### Vercel
Create a pull request or push to main to create a vercel deployment. To configure the vercel deployment, edit the YAML files within the directory "github\workflows".

&nbsp;
### Heroku
- Deploying to heroku
```
git push thinkSlice main
```
- Checking heroku logs
```
heroku logs --tail
```
&nbsp;

## Dependencies Guide
Here are the important dependencies for this project.

&nbsp;
### PostgreSQL
PostgreSQL is the database for this project.
- Download the CLI psql/ GUI pgAdmin 4
- To access the tables in this project, prefix "public" to their respective table names. 
```
SELECT * from public."userVideos_video"
```

&nbsp;
### Local Redis/Docker Installation
Redis is used for the chat application as well as for caching.
- Starting a redis server
```
docker run -p 6379:6379 -d redis:5
```
- Use Docker Desktop to start/stop the server

&nbsp; 
### MUX API
Mux API is used for the videos. 
- Access the python documentation here: https://github.com/muxinc/mux-python
- Access their dashboard here: https://dashboard.mux.com/login

&nbsp;
### AWS S3/Cloudfront
- Access AWS console here: https://signin.aws.amazon.com/signin?redirect_uri=https%3A%2F%2Fconsole.aws.amazon.com%2Fconsole%2Fhome%3Ffromtb%3Dtrue%26hashArgs%3D%2523%26isauthcode%3Dtrue%26nc2%3Dh_ct%26src%3Dheader-signin%26state%3DhashArgsFromTB_us-east-1_3b278fbf8f6b11a6&client_id=arn%3Aaws%3Asignin%3A%3A%3Aconsole%2Fcanvas&forceMobileApp=0&code_challenge=LZCfu_tD8d8dReRATHvJ-zHvngU21ZaBLlsWkdVt7tM&code_challenge_method=SHA-256

- Access django-storages documentation here: https://django-storages.readthedocs.io/en/latest/
You can edit configuration within settings.py file.

&nbsp;

