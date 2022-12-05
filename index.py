import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta
app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>李幸諭Python網頁</h1>"
    homepage += "<br><a href=/read>讀取Firestore資料</a><br>"
    homepage += "<br><a href=/webhook>查詢電影</a><br>"
    return homepage

@app.route("/read", methods=["GET", "POST"])
def read():
    if request.method == "POST":
        cond = request.form["keyword"]
        tea = request.form["teacher"]
        result = "請輸入您要查詢的課程關鍵字："+ cond
        result = "請輸入您要查詢的教師關鍵字："+ tea
        db = firestore.client()
        collection_ref = db.collection("111")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if cond in dict["Course"] and tea in dict["Leacture"]:
                result += dict["Leacture"]+"老師開的"+dict["Course"]+"課程，每周"+dict["Time"]+"於"+dict["Room"]+"上課<br>"
        if result == "":
            result = "抱歉，查無相關條件的選修課程"
        return result
    else:
        return render_template("read.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    msg =  req.get("queryResult").get("queryText")
    info = "動作：" + action + "； 查詢內容：" + msg
    return make_response(jsonify({"fulfillmentText": info}))


#if __name__ == "__main__":
#    app.run()
   