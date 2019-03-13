# Item Catalog Udacity Project
By Munnaluri Krishna Sravanthi
This web app is a project for the Udacity [FSND Course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## About the project
This project is a RESTful web application utilizing the Flask framework which accesses a SQL database that populates Film categories and their editions. OAuth2 provides authentication for further CRUD functionality on the application. Currently OAuth2 is implemented for Google Accounts.

##  This Project contains
This project has one main Python module `Film.py` which runs the Flask application. 
A SQL database is created using the `Film_Setup.py` module
you can populate the database with test data using `Film_database_init.py`.
The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application.

## Skills Required
1. Python
2. HTML
3. CSS
4. OAuth
5. Flask Framework
6. DataBaseModels
## Installation
There are some dependancies and a few instructions on how to run the application.
Seperate instructions are provided to get GConnect working also.

## Dependencies
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)



## How to Install
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repo or download and place zip here
3. Launch the Vagrant VM (`vagrant up`)
4. Log into Vagrant VM (`vagrant ssh`)
5. Navigate to `cd /vagrant` as instructed in terminal
6. The app imports requests which is not on this vm. Run pip install requests
7. Setup application database `python /Films Collection/Film_Setup.py`
8. Insert sample data `python /Films Collection/Film_database_init.py`
9. Run application using `python /Films Collection/Films.py`
10.Access the application locally using http://localhost:4444

After running the project
--------------------------
--------------------------

By clicking the login button gconnect will open.
I have generated client_secrets.json file I have secret key through which we can access the mail and login in it.

By login into the films hub a message will be displayed that welcome to film store.
Now click on the films hub then it will display a slideshow of some images.
After click on the film categories it will display film items.
In displaying film items we will have edit and dedlete buttons,edit-we will edit the film details,delete-we will delete the film details which we want to delete.
when we want to edit and delete the film category there are buttons beside and click them to edit and delete.
when we want to add a new film category click add film category and add category and then click submit button.
These are the operations we will perform.


*Optional step(s)

## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'Films Collection'
7. Authorized JavaScript origins = 'http://localhost:4444'
8. Authorized redirect URIs = 'http://localhost:4444/login' && 'http://localhost:4444/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in films collection directory that you cloned from here
14. Run application.

## JSON Endpoints
The following are open to the public:

1.allFilmsJSON: `/FilmStore/JSON`
    - Displays all the Films.

2.categoriesJSON: `/filmStore/filmCategories/JSON`
    - Displays all Films categories
	
3.itemsJSON: `/filmStore/films/JSON`
	- Displays all Film Items

4.categoryItemsJSON: `/filmStore/<path:film_name>/films/JSON`
    - Displays Film Items for a specific Film category

5.ItemJSON: `/filmStore/<path:film_name>/<path:edition_name>/JSON`
    - Displays a specific Film category .

## Miscellaneous

This project is inspiration from [gmawji](https://github.com/gmawji/item-catalog).
