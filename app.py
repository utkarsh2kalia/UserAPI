from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask import jsonify
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'userdetails'

mysql = MySQL(app)




@app.route('/app/user', methods=['POST'])
def createLogin():
    userdata = request.json
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (userdata['username'], userdata['password']))
    mysql.connection.commit()
    cur.close()
    return jsonify(status='account created')


@app.route('/app/user/auth', methods=['POST'])
def authLogin():
    userdata = request.json
    cur = mysql.connection.cursor()
    query = "SELECT userid, password FROM users WHERE username = '{}'".format(userdata['username'])
    cur.execute(query)
    passdata = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    if userdata['password']== passdata[0][1]:

        return jsonify(status='SUCCESS', userid=passdata[0][0])
    else:

        return jsonify(status='FAILED')


@app.route('/app/sites/list', methods=['GET'])
def getWebsites():
    userid = request.args.get('user')
    cur = mysql.connection.cursor()
    query = "SELECT website, username, password FROM usercred WHERE userid = '{}'".format(userid)
    cur.execute(query)
    userdata = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return jsonify(userdata)


@app.route('/app/sites/list', methods=['POST'])
def setWebsitesData():
    userid = request.args.get('user')
    userdata = request.json
    cur = mysql.connection.cursor()
    query = "update usercred set username = '{}', password= '{}' WHERE userid = {} and website='{}'".format(userdata['username'], userdata['password'],userid, userdata['website'])
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    return jsonify('Success')

if __name__ == '__main__':
    app.run()