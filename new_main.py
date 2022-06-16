from crypt import methods
from unittest import result
from flask import request, Flask, jsonify

import psycopg2

app = Flask(__name__)

conn = psycopg2.connect("dbname='crm' user='silvanakoharian' host='localhost'")
cursor = conn.cursor()

def create_all():
  cursor.execute ('''
   CREATE TABLE IF NOT EXISTS Organizations (
      org_id serial PRIMARY KEY,
      name VARCHAR NOT NULL,
      phone VARCHAR,
      city VARCHAR,
      state VARCHAR,
      active smallint
  );
  ''')

  conn.commit()

  cursor.execute("SELECT name FROM Organizations WHERE name = 'DevPipeline';")
  results = cursor.fetchone()

  org_id = -999

  if not results:
    cursor.execute("""
        INSERT INTO Organizations
          (name, phone, city, state, active) VALUES
          ('DevPipeline', '7894567893', 'Orem', 'UT', 1)
        RETURNING org_id;
        """)
    
    conn.commit()
    org_id = cursor.fetchone()[0]
    
  
  
  cursor.execute ('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id serial PRIMARY KEY,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR,
        email VARCHAR UNIQUE NOT NULL,
        phone VARCHAR,
        city VARCHAR,
        state VARCHAR,
        org_id int,
        active smallint
    );
    ''')


  conn.commit()

  cursor.execute("SELECT email FROM Users WHERE email = 'admin@devpipeline.com';")
  results = cursor.fetchone()

  if not results:
    cursor.execute("""
        INSERT INTO Users
        (first_name, last_name, email, phone, city, state, org_id, active) VALUES
        ('Super', 'Admin', 'admin@devpipeline.com', '8018018011', 'Orem', 'UT', %s, 1);
        """, [org_id,])
    conn.commit()




# add user
@app.route('/user/add', methods=['POST'])
def add_user():
  form = request.form

  fields = ["first_name", "last_name", "email", "phone", "city", "state", "org_id", "active"]
  req_fields = ["first_name", "email"]
  values = []

  for field in fields:
    form_value = form.get(field)
    if form_value in req_fields and form_value == " ":
      return jsonify (f'{field} is required field'), 400

    values.append(form_value)

  cursor.execute('''INSERT INTO Users (first_name, last_name, email, phone, city, state, org_id, active) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', values)

  conn.commit()
  return jsonify('User Added'), 200





# # update user's information
@app.route('/user/edit/<user_id>', methods=['PUT'])
def edit_user(user_id, first_name = None, last_name = None, email = None, password = None, city= None, state = None, active = None):
    cursor.execute('SELECT user_id,first_name, last_name, email, phone, city, state, org_id, active FROM Users WHERE user_id = %s', (user_id,))
    result = cursor.fetchone()
    print(result)
    set_clauses = []        
    update_values = []

    fields = ["first_name", "last_name", "email", "phone", "city", "state", "org_id", "active"]

    if result:
        form = request.form
        for field in fields:
          form_value = form.get(field)
          if form_value !=None:
            set_clauses.append(f'{field} = %s')
            update_values.append(form_value)

        set_clause_string = ' , '.join(set_clauses)
        update_values.append(str(user_id))
        query_str = f'UPDATE Users SET {set_clause_string} WHERE user_id = %s'
        cursor.execute(query_str, update_values)
        conn.commit()
        return jsonify('User Updated'), 201
    return ('User not found'), 404




# get user by id
@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
  cursor.execute('SELECT user_id,first_name, last_name, email, phone, city, state, org_id, active FROM Users WHERE user_id = %s', (user_id,))
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
      'org_id': result[7],
      'active' : result[8]
    }

    return jsonify(result_dictionary), 200
  return('User not found'), 404





# get all users
@app.route('/user/list', methods=['GET'])
def get_all_users():
    output_json ={}

    list_of_users = []

    cursor.execute('''SELECT u.user_id, u.first_name, u.last_name, u.email, u.phone, u.city, u.state, u.org_id, u.active,
                             o.org_id, o.name, o.phone, o.city, o.state, o.active
                      FROM Users  u
                      JOIN Organizations o
                      ON o.org_id = u.org_id;
                      ''')

    results = cursor.fetchall()


    for user in results:
      new_record = {
      'user_id' : user[0],
      'first_name' : user[1],
      'last_name' : user[2],
      'email': user[3],
      'phone': user[4],
      'city' : user[5],
      'state' : user[6],
      'active' : user[8],
      'organization': {
        'org_id': user[9],
        'name': user[10],
        'phone': user[11],
        'city': user[12],
        'state': user[13],
        'active': user[14],
         }
      }

      list_of_users.append(new_record)

      output_json = {"results": list_of_users}

    return jsonify(output_json), 200





# # Delete an user
@app.route('/user/delete/<user_id>', methods=['DELETE'])
def user_delete(user_id):
  cursor.execute('SELECT user_id,first_name, last_name, email, phone, city, state, org_id, active FROM Users WHERE user_id = %s', (user_id,))
  result = cursor.fetchone()
  print("booo", result)
  if result:
     cursor.execute('DELETE FROM Users WHERE user_id = %s',(user_id,))
     conn.commit()
     return jsonify('User Deleted'), 200
  return jsonify('User not found'), 404
  




# # Search for a key word in user's data
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
  create_all()
  app.run()
