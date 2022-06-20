from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import boto3
import base64
import json

app = Flask(_name_)

session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name= "ap-south-1"
)

get_secret_value_response = client.get_secret_value(
    SecretId = "prod/mydb/hidatabase"
)
if 'SecretString' in get_secret_value_response:
    secret = get_secret_value_response['SecretString']
else:
    secret = decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
secretdict = json.loads(secret)

 
app.config['MYSQL_HOST'] = secretdict['host']

app.config['MYSQL_USER'] = secretdict['username']
  
app.config['MYSQL_PASSWORD'] = secretdict['password']
 
app.config['MYSQL_DB'] = secretdict['dbname']
 
mysql = MySQL(app) 

@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''',(name,age))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"
        
if _name_ == "_main_":
   app.run(host='0.0.0.0', port=80)
