# Project Trivia
#### Udacity Trivia API project

### Full Stack Trivia
Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.
This app allows users to challenge themselves from trivia questions and seeing who's the most knowledgeable of the bunch.

## Features:
- View questions. Questions are grouped into categories (visible on the left category "menu". Questions are also displayed by category. - Users can also show/hide the answer to each question.
- Add and delete questions
- Search for questions based on a text query string.
- Play the quiz game, randomizing either all questions or within a specific category.

## Architecture
The application is structured as thus
- /backend - Flask

- /frontend - React

## Environment Variables and Database Connection
Postgres was used as the database backend. You may configure any database backend you want to use in the 'database' varaible in models.py, located in the /backend/ folder

Other environment variables can be configured by creating a .env file in the /backend/ folder (optional)

## Run the application
To run the backend, you would need to navigate to the /backend/ folder and run `flask run`
To run the frontend, you would need to navigate to the /frontend/ folder and run the commands below (You need node to be able to run this - kindly install node from nodejs.org if you don't have node/npm already)

`npm install`

`npm start`
