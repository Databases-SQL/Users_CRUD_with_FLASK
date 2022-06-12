# Users_CRUD_with_FLASK
 Backend Homework - Create a back-end application that implements all of the CRUD features for a "User" account.
 
 
 =======================
Assignment
=======================

Create a back-end application that implements all of the CRUD features for a "User" account.

Test your API's with Postman.

The User account should be a database table that contains the following fields:

CREATE TABLE IF NOT EXISTS Users (
   user_id serial PRIMARY KEY,
   first_name VARCHAR NOT NULL,
   last_name VARCHAR,
   email VARCHAR NOT NULL,
   password VARCHAR NOT NULL,
   city VARCHAR,
   state VARCHAR,
   active BOOLEAN DEFAULT true
);


1) Add a user  "/user/add" POST
   Adds a user to the database. The POST endpoint should accept the fields for the user as form fields.
   If the POST does not contain required fields, then return an appropriate error.

2) Edit a user "/user/edit/<user_id>" POST
   Edits the user object with the id <user_id>.  The POST endpoint should accept the fields for the user as form fields.
   If the user with id <user_id> does NOT exist, an error code of 404 should be returned.

3) Delete a user "/user/delete/<user_id>" DELETE 
   Deletes the user with the id <user_id>
   If the user with id <user_id> does NOT exist, an error code of 404 should be returned.

4) Get a user "/user/<user_id>" GET 
   Returns a JSON dictionary of a single user with the id of <user_id>
   If the user with id <user_id> does NOT exist, an error code of 404 should be returned.

5) Get a list of all users "/user/list" GET
   Returns a JSON with a List of Dictionaries, with each user represented by a dictionary
   
   If there are no users in the database, this should return a JSON of an empty list.
   
   
   
====================
Extra Credit
====================

Implement a /user/search/<search_term>   that will search first_name, last_name, city, state, email. If the any of the fields match the search_term (LIKE '%search_term%'), then return them. This will be a dictionary with on element called "results" that is a list of search results.

Make it case-insensitive.
   
   
   
