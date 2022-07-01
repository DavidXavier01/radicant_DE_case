# %% Connecting

from datetime import datetime
from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'etfs'
 
mysql = MySQL(app)

# %% 
@app.route('/filter_funds', methods = ['GET','POST'])
def filter():
    # Request Params
    id_fund_category = request.args.get('id_fund_category')
    id_size_type = request.args.get('id_size_type')
    
    # Param check
    if not id_fund_category or not id_fund_category:
        return "Fill the requested params"
    
    if request.method == "POST":

         # MySQL conn
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO request (id_fund_category, id_size_type, date) VALUES(%s,%s,%s)",(id_fund_category,id_size_type,datetime.now()))
        mysql.connection.commit() 
        
        # Close
        cursor.close()

        return "Query saved"

    if request.method == "GET":

        # MySQL conn
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT fund_symbol, fund_category, size_type FROM esg_filter_funds WHERE id_size_type = %s and id_fund_category = %s",(id_fund_category,id_size_type))

        # Fetch and close
        result = cursor.fetchall()
        cursor.close()
       
        # Return
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')