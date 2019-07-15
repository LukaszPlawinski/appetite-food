# Appetite Food

![alt text](https://github.com/LukaszPlawinski/appetite-food/blob/master/static/img/thumnail.jpg)


## UX

This website is created for users who loves cooking and healthy food. User can find here a lot of recipes with images and the way of preparation.
Searching and category  inputs make it much easier. After logging in he can add, edit and delete recipe through user friendly interface.
Project design and data base structure are in main folder.

### User stories:
-As a person who loves cooking i would like to find fresh and healthy recipes.
 I should be able to add my own recipes too.
 
### Acceptance Criteria:

* Recipe should contain:
    * name
    * picture
    * author
    * description
    * ingredients
    * way of preparation
* Possibility to find/filter reciepes:
    *  by category
    *  by searched phrase
* Logged person should be able to:
    * add recipe
    * edit only own recipe
    * delete only own recipe
* Possibility to contact website owner through social links or contact form




## Features
### All pages
    On all pages there is a navbar where are links to: 
        1.Home
        2.Login/Logout option
            - When user clicks it, modal window appears. There he has option to login or register. 
              Password is encrypted.
        3.Contact
        4.Add recipe - just for logged users
    In a footer there are social icons  leading to:
        1.Instagram
        2.Github
        3.Linkedin
### Home page
    1.All recipes are displayed (image and name of the recipe)
    2.User can chose food category:
        * Starters
        * Main courses
        * Desserts
        * Drinks & Smoothies
    3. User can search recipe by phrase using searching input
### Meal page
    1.Recipe name
    2.Recipe author
    3. Icons to edit and delete recipe (Just if you are logged in and it is your recipe)
    4. Ingredienta list
    5. Description
    6. Preparation steps
### Add recipe
    Page contain form where user can add all necessary informations about recipe.
### Edit page 
    User can edit all informations about recipe
### Contact page
    In case that user would like to contact website owner he can fill up form which contains:
        * Name
        * Tel number
        * Email
        * Message
    All information are automatically sent to owner email.
    
    


## Technologies Used

1. HTML5 - Valid HTML structure
2. CSS3 - Styling for page
3. Javascript - makes website interactive, helps in building readable charts
4. JQUERY - form verification, rendering
5. Bootstrap-  mobile responsive layout, elements such as modals, cookie alert
6. PYTHON - logic, routes
7. FLASK - login, searching
8. Pymongo - CRUD operations
9. Flask-email - email automation
10. Bcrypt - password hashing
11. MongoDB-  database management
12. MongoAtlas- automated cloud MongoDB service where database is stored
13. [Font Awsome](https://fontawesome.com/) - edit, delete and cosial icons
14. [Autoprefixer](https://autoprefixer.github.io/)- plugin which add vendor prefixes for different browsers
15. Balsamic Mockups 3 - to create mockup


## Testing
* Html files were tested by [HTML VALIDATOR](https://validator.w3.org/)
* Css files were tested by [CSS Validator](https://jigsaw.w3.org/css-validator/)
* Javascript files were tested by [JS Validator](https://codebeautify.org/jsvalidate)
    and [jshint](https://jshint.com/)
* Python file was tested by [Python validator](https://pythonbuddy.com/)
* All inputs, links and buttons have been tested
* Tested features:
    * Register user , user exist error
    * Login user, Wrong Login, Wrong Password
    * Logout 
    * Add recipe
    * Edit recipe
    * Delete recipe
    * Search by phrase
    * Search by category
    * Contact form
* Website is responsive at all screen resolutions. 
* Website works on mobiles such as:
    * Iphone 6/7/8
    * Iphone 6/7/8 plus
    * Samsung galaxy s5
    * Pixel 2
* Website was tested in 'MultiBrowser' - cross-browser testing program. App works in all browsers below:
    * Chrome (Versions 75)
    * Firefox (Version 68)
    * Opera (Version 62)
    * MS Edge (Version 42)
    * Safari (Version 11)


## Deployment

* I was using cloud 9 IDE and git bash command line which helped me to commit ale changes on "Deployment" branch.
* I installed Flask and all necessary extensions
* All frameworks/extensions which have to be installed in environment are in requirements.txt file.
* Main folder contain Procfile which declaring what commands are run by application’s dynos on the Heroku platform.
* After everything worked I merged "deployment" branch with "Master" branch.
* Code was pushed to github repository and later on connected with heroku pipeline.
* In heroku environment i saved variables such us: "MONGO_URI", "MAIL_USER", "MAIL_PASSWORD"
* Right know fully deployed website is visible on heroku server.

### [Live website ](https://appetite-food.herokuapp.com/)
### [Github repository](https://github.com/LukaszPlawinski/appetite-food)


## Credits
* Background pictures are from: [Pexels](https://data.gov.ie/)
* Recipes and recipe images come from [SkinnyMS](https://skinnyms.com/)
* [Cookie alert](https://github.com/Wruczek/Bootstrap-Cookie-Alert)
