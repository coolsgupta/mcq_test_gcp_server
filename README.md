# MCQ test taking tool

## Frameworks Used
  Frontend: React
  <br>
  Backend: Flask

## Deployment Server
  Google App Engine Standard Environment for Python

### Frontend: https://mcq-test-tool.wl.r.appspot.com/

### Backend: https://test-taking-tool.wl.r.appspot.com]

## Backend
### Structure
  1. main.py: Contains the routes for APIs.
  2. handlers.py: The respective handlers for the defined routes.
  3. utils.py: Supporting utils and Memcache handling class.
  4. data_models.py: Google Datastore Data Models used to manage data at backend.

### deployment on local server
#### components required:
  1. Google cloud SDK
  2. Google cloud sdk supporting extensions for python

#### steps
  1. Go to the main project home directory (the one containing app.yaml).
  2. Open Terminal, run command "dev_appserver.py app.yaml"

### Frontend
  1. ReactApp/src/App.js: contains the app configuration and respective routes for the react app.
  2. ReactApp/src/components: Contains supporting components for each page.
  3. ReactApp/src/components/Login.js: Collects user info: User Email used for to manage user data.
  4. ReactApp/src/components/MainPage.js: Serves the homepage with the operation to attempt the test category wise and displays all previous score report.
  5. ReactApp/src/components/TakeTest.js: Serves the Test page to the user in mcq format with a submit button to submit the test and get the score report(loaded on the main page).

### deployment on local server
#### components required
  1. Node

#### steps
  1. Go to the main project home directory ReactApp/.
  2. run "npm i"
  3. In src/components/Constant.js check server address to be local (update the development server as the respective local host for backend).
  4. run "npm start"


## Possible Improvements
1. Google Login: To streamline login process (requiring only one time login per user and bypassing the login page if the user is already logged in)
2. UI: working with bootstrap templates to extend material design to the main page and the test pages.
3. Navigation bar on the test page to allow quick review of attempted questions and jump to a selected question on the test page.
4. A timer showing the time taken to attempt the test.
5. Handling the inner html provided in the question text.
