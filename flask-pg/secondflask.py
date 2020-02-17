# from app import resource
import psycopg2
from flask import Flask, jsonify, request
# from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(
        database="postgres", user="postgres", password="tongji2018openedu", host="202.120.167.50", port="5432")


@app.route('/rest/anon/tasks/add/<string:begintime>/<string:endtime>/<string:description>/<string:state>',methods=['POST'])
def create(begintime,endtime,description,state):
    cur = conn.cursor()
    data = request.get_json()
    print(begintime)
    print(endtime)
    print(description)
    print(state)
    cur.execute("insert into taskone(begintime,endtime,description,state) values(%s,%s,%s,%s)",
             (begintime, endtime,description,state))
    conn.commit()
    return "1"


@app.route('/rest/anon/tasks',methods=['GET'])
def read():
    cur = conn.cursor()
    
    cur.execute(
        "select * from taskone")
    rows = cur.fetchall()
    l = []
    for row in rows:
        print(row)
        dic= {'id': str(row[0]),'description': str(row[1]),'begintime':str(row[2]),'endtime':str(row[3]),'state':str(row[4])}
        l.append(dic)
    return jsonify(l)


@app.route('/rest/anon/tasks/getByState/<string:state>',methods=['GET']) 
def read_state(state):
    cur = conn.cursor()
    
    cur.execute(
        "select * from taskone where state="+state)
    rows = cur.fetchall()
    l = []
    for row in rows:
        dic= {'id': str(row[0]),'description': str(row[1]),'begintime':str(row[2]),'endtime':str(row[3]),'state':str(row[4])}
        l.append(dic)
    return jsonify(l)



@app.route('/rest/anon/tasks/edit/<string:begintime>/<string:endtime>/<string:description>/<string:state>/<string:dId>', methods=['POST'])
def update(begintime,endtime,description,state,dId):
    cur = conn.cursor()
    data = request.get_json()

    cur.execute("UPDATE taskone SET state = "+state+",description = '"+description+"', begintime = '"+begintime+"', endtime ='"+endtime+"'  WHERE id = " + dId);

    conn.commit()
    return "1"

@app.route('/rest/anon/tasks/editState/<string:state>/<string:dId>', methods=['POST'])
def update_state(state,dId):
    cur = conn.cursor()
    data = request.get_json()

    cur.execute("UPDATE taskone SET state = "+state+" WHERE id = " + dId);

    conn.commit()
    return "1"


@app.route('/rest/anon/tasks/delete/<string:id>', methods=['GET'])
def delete(id):
    cur = conn.cursor()
    cur.execute("DELETE from taskone where id="+ id)
    conn.commit()
    
    return "1"


# def create_app():
#     app = Flask(__name__)
#     CORS(app)
#     app.secret_key = ""
#     api = Api(app)
#     app.add_resource(resource.ResourceUser,"/")

#     return app

if __name__ == '__main__':
    # app = create_app()
    app.run()
