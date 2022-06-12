from crypt import methods
from flask import request, Flask, jsonify, Response

import psycopg2

app = Flask(__name__)

conn = psycopg2.connect("dbname='usersource' user='silvanakoharian' host='localhost'")
cursor = conn.cursor()


# add user
@app.route('/user/add', methods=['POST'])
def add_user():
  form = request.form
  first_name = form.get('first_name')
  if first_name == '':
    return jsonify('first name is required!'), 400
  last_name = form.get('last_name')
  email = form.get('email')
  if email == '':
    return jsonify('email is required!'), 400
  password = form.get('password')
  if password == '':
    return jsonify('password is required!'), 400
  city = form.get('city')
  state = form.get('state')

  cursor.execute('INSERT INTO Users (first_name, last_name, email, password, city, state) VALUES (%s, %s, %s, %s, %s, %s)',[first_name, last_name, email, password, city, state])

  conn.commit()
  return jsonify('User Added'), 200





# update user's information
@app.route('/user/edit/<user_id>', methods=['PUT'])
def edit_user(user_id, first_name = None, last_name = None, email = None, password = None, city= None, state = None, active = None):
    cursor.execute('SELECT user_id,first_name, last_name, email, password, city, state, active FROM Users WHERE user_id = %s', (user_id,))
    result = cursor.fetchone()
    print(result)
    set_clauses = []        
    update_values = []

    if result:
        form = request.form
        first_name = form.get('first_name')
        if first_name != None:
          set_clauses.append('first_name = %s') 
          update_values.append(first_name)

        last_name = form.get('last_name')
        if last_name != None:
          set_clauses.append('last_name = %s') 
          update_values.append(last_name)

        email = form.get('email')
        if email != None:
          set_clauses.append('email = %s') 
          update_values.append(email)

        password = form.get('password')
        if password != None:
          set_clauses.append('password = %s') 
          update_values.append(password)

        city = form.get('city')
        if city != None:
          set_clauses.append('city = %s') 
          update_values.append(city)

        state = form.get('state')
        if state != None:
          set_clauses.append('state = %s') 
          update_values.append(state)

        active = form.get('active')
        if active != None:
          set_clauses.append('active = %s') 
          update_values.append(active)


        set_clause_string = ' , '.join(set_clauses)

        query_str = f'UPDATE Users SET {set_clause_string} WHERE ' + 'user_id = %s'
        print (query_str)
        print(set_clause_string)
        print(update_values)
        cursor.execute(query_str, update_values)
        conn.commit()
        return jsonify('User Updated'), 201
    return ('User not found'), 404




# get user by id
@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
  cursor.execute('SELECT user_id,first_name, last_name, email, password, city, state, active FROM Users WHERE user_id = %s', (user_id,))
  result = cursor.fetchone()
  print(result)

  if result:

    result_dictionary = {
      'user_id' : result[0],
      'first_name' : result[1],
      'last_name' : result[2],
      'email': result[3],
      'password': result[4],
      'city' : result[5],
      'state' : result[6],
      'active' : result[7]
    }

    return jsonify(result_dictionary), 200
  return('User not found'), 404





# get all users
@app.route('/user/list', methods=['GET'])
def get_all_users():
    cursor.execute('SELECT user_id,first_name, last_name, email, password, city, state, active FROM Users')
    results = cursor.fetchall()

    list_of_users = []

    for user in results:
      list_of_users.append(
        {
      'user_id' : user[0],
      'first_name' : user[1],
      'last_name' : user[2],
      'email': user[3],
      'password': user[4],
      'city' : user[5],
      'state' : user[6],
      'active' : user[7]
    })

    output_dictionary ={
      "users" : list_of_users
    }

    return jsonify(output_dictionary), 200





# Delete an user
@app.route('/user/delete/<user_id>', methods=['DELETE'])
def user_delete(user_id):
  cursor.execute('SELECT user_id,first_name, last_name, email, password, city, state, active FROM Users WHERE user_id = %s', (user_id,))
  result = cursor.fetchone()
  print("booo", result)
  if result:
     cursor.execute('DELETE FROM Users WHERE user_id = %s',(user_id,))
     conn.commit()
     return jsonify('User Deleted'), 200
  return jsonify('User not found'), 404
  




# Search for a key word in user's data
@app.route('/user/search/<search_term>', methods=['GET'])
def user_search(search_term):
  search_term = search_term.lower()
  cursor.execute('''SELECT first_name, last_name, city, state, email 
                     FROM Users 
                     WHERE LOWER(first_name) LIKE %s
                     OR LOWER(last_name) LIKE %s
                     OR LOWER(city) LIKE %s
                     OR LOWER(state) LIKE %s
                     OR LOWER(email) LIKE %s
                     ''',
                     (f'%{search_term}%',f'%{search_term}%',f'%{search_term}%',f'%{search_term}%',f'%{search_term}%')
                     )
  results = cursor.fetchall()

  if results:
    list_of_search_results = []

    for result in results:
          list_of_search_results.append( {
         'first_name' : result[0],
         'last_name' : result[1],
         'city' : result[2],
         'state' : result[3],
         'email' : result[4],
      } )

    output_dictionary = {
      "results" : list_of_search_results
   }
    return jsonify(output_dictionary), 200

  return jsonify('Search term not found'), 404





if __name__=='__main__':
  app.run()

# CREATE TABLE IF NOT EXISTS Users (
#    user_id serial PRIMARY KEY,
#    first_name VARCHAR NOT NULL,
#    last_name VARCHAR,
#    email VARCHAR UNIQUE NOT NULL,
#    password VARCHAR NOT NULL,
#    city VARCHAR,
#    state VARCHAR,
#    active BOOLEAN DEFAULT true
# );