from flask import Flask, render_template, request,redirect,session,url_for
from pymongo import MongoClient
import pandas
import csv
import json
from bson.json_util import dumps
from bson import json_util
import base64
import gridfs


datas = [
    {
        'author': 'Darshan',
        'title': 'CO Mapping'
    }
]

################################################################# Database Section ################################################################
demo = MongoClient()
myclient = MongoClient('localhost', 27017)


db = myclient["Collage"]  # db name
collection = db["StudentDetails"]  # collection name
fs = gridfs.GridFS(db)

################################################################ End of Data Base section #######################################################

app = Flask(__name__)

app.secret_key = "Darshan"

# @app.route("/")
# def index():
#     return render_template("index.html")


# #################################################### Image Upload section ############################################################
@app.route("/upload_image")
def img():
    return render_template("upload_image.html")


@app.route("/upload", methods=['POST','GET'])
def upload():
    if 'mse' in session:
        if 'year' in session:
            if 'semister' in session:
                if request.method == 'POST':
                    db.collection.drop()
                    print ("Hello")
                    csvfilepath = request.form["file"]
                    print(csvfilepath)
                    with open(csvfilepath, "r") as csvfile:
                        csvreader = csv.DictReader(csvfile)
                        for csvrow in csvreader:
                        # USN = csvrow["USN"]
                        # data[USN] = csvrow
                            db.collection.insert_one(csvrow)
                return render_template("index.html")
        return "Session is not logged in"
    return redirect(url_for("login"))

@app.route("/session", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        mse = request.form['mse']
        year = request.form['year']
        semister = request.form['semister']
        session['mse'] = mse
        session['year'] = year
        session ['semister'] = semister
        return redirect(url_for("upload"))
    return render_template("session.html")

@app.route("/result")
def result():
    semister = session['semister']
    mse = session['mse']
    year = session['year']
    
    total = db.collection.distinct("usn")
    total_pandas = pandas.Series(total)
    total_count = total_pandas.count()
    result = db.collection.find({"sem": semister, "mse": mse, "year": year})
    
    fail = db.collection.find( { "marks": { "$in": ["0","1","2","3","4","5","6","7","8","9","10","11","12"]}})
    pand_fail = pandas.Series(list(fail))
    count_fail = pand_fail.count()
    print(count_fail)
    
    passed = db.collection.find( { "marks": { "$in": ["12","13","14","15","16","17","18","19","20","21","22","23","24","25"]}})
    pand_pass = pandas.Series(list(passed))
    count_pass = pand_pass.count()
    print(count_pass)
    
    return render_template("student.html",database=result,semister=semister,mse=mse,year=year,total_count=total_count,total=total,count_pass=count_pass,count_fail=count_fail)


@app.route("/export")
def export_csv():
    with open('names.csv', 'w', newline='') as csvfile:
        fieldnames = ['first_name', 'last_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
        writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
        writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
    return "success"






@app.route("/charts", methods=['POST', 'GET'])
def chart():
    semister = session['semister']
    mse = session['mse']
    year = session['year']
    subjects = db.collection.distinct("subject")
    distinction = db.collection.find( { "marks": { "$in": ["25","26","27","28","29","30"]}})
    
    first_class = db.collection.find( { "marks": { "$in": ["19","20","21","22","23","24","25"]}})
    second_class = db.collection.find( { "marks": { "$in": ["12","13","14","15","16","17","18",]}})
    fail = db.collection.find( { "marks": { "$in": ["0","1","2","3","4","5","6","7","8","9","10","11","12"]}})
    
    pand_distinction = pandas.Series(list(distinction))
    count_distinction = pand_distinction.count()
    print(count_distinction)
    
    pand_first_class = pandas.Series(list(first_class))
    count_first_class = pand_first_class.count()
    print(count_first_class)
    
    pand_second_class = pandas.Series(list(second_class))
    count_second_class = pand_second_class.count()
    print(count_second_class)
    
    pand_fail = pandas.Series(list(fail))
    count_fail = pand_fail.count()
    print(count_fail)
        
    data = pandas.Series(list(subjects))
    count = data.count() - 1
    subject_count = count
    if subject_count == 1:
        return "Minimum 4 Subject is Required"
    if subject_count == 2:
        return "Minimum 4 Subject Required"
    if subject_count == 3:
        return "Minimum 4 Subject Required"
    if subject_count == 4:
        s1_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[0]})
        s1 = pandas.Series(s1_cursor)
        s1.to_dict()
        s1_count = s1.count()
        
        s2_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[1]})
        s2 = pandas.Series(s2_cursor)
        s2.to_dict()
        s2_count = s2.count()
        
        s3_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[2]})
        s3 = pandas.Series(s3_cursor)
        s3.to_dict()
        s3_count = s3.count()
        
        s4_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[3]})
        s4 = pandas.Series(s4_cursor)
        s4.to_dict()
        s4_count = s4.count()
        
        s5_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[4]})
        s5 = pandas.Series(s5_cursor)
        s5.to_dict()
        s5_count = s5.count()
        marks = db.collection.find()          
        return render_template("charts.html",subject_count=subject_count,distinction=distinction,subjects=subjects,count_distinction=count_distinction,count_first_class=count_first_class,count_second_class=count_second_class,count_fail=count_fail,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s1_count=s1_count,s2_count=s2_count,s3_count=s3_count,s4_count=s4_count,s5_count=s5_count)

    if subject_count == 5:
        s1_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[0]})
        s1 = pandas.Series(s1_cursor)
        s1.to_dict()
        s1_count = s1.count()
        
        s2_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[1]})
        s2 = pandas.Series(s2_cursor)
        s2.to_dict()
        s2_count = s2.count()
        
        s3_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[2]})
        s3 = pandas.Series(s3_cursor)
        s3.to_dict()
        s3_count = s3.count()
        
        s4_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[3]})
        s4 = pandas.Series(s4_cursor)
        s4.to_dict()
        s4_count = s4.count()
        
        s5_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[4]})
        s5 = pandas.Series(s5_cursor)
        s5.to_dict()
        s5_count = s5.count()
        
        s6_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[5]})
        s6 = pandas.Series(s6_cursor)
        s6.to_dict()
        s6_count = s6.count()
        marks = db.collection.find()            
        return render_template("charts.html",subject_count=subject_count,subjects=subjects,distinction=distinction,first_class=first_class,count_distinction=count_distinction,count_first_class=count_first_class,count_second_class=count_second_class,count_fail=count_fail,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s1_count=s1_count,s2_count=s2_count,s3_count=s3_count,s4_count=s4_count,s5_count=s5_count,s6_count=s6_count)

        
    if subject_count == 6:
        s1_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[0]})
        s1 = pandas.Series(s1_cursor)
        s1.to_dict()
        s1_count = s1.count()
        
        s2_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[1]})
        s2 = pandas.Series(s2_cursor)
        s2.to_dict()
        s2_count = s2.count()
        
        s3_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[2]})
        s3 = pandas.Series(s3_cursor)
        s3.to_dict()
        s3_count = s3.count()
        
        s4_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[3]})
        s4 = pandas.Series(s4_cursor)
        s4.to_dict()
        s4_count = s4.count()
        
        s5_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[4]})
        s5 = pandas.Series(s5_cursor)
        s5.to_dict()
        s5_count = s5.count()
        
        s6_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[5]})
        s6 = pandas.Series(s6_cursor)
        s6.to_dict()
        s6_count = s6.count()
        
        s7_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[6]})
        s7 = pandas.Series(s7_cursor)
        s7.to_dict()
        s7_count = s7.count()
        marks = db.collection.find()            
        return render_template("charts.html",subject_count=subject_count,subjects=subjects,count_distinction=count_distinction,count_first_class=count_first_class,count_second_class=count_second_class,count_fail=count_fail,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s1_count=s1_count,s2_count=s2_count,s3_count=s3_count,s4_count=s4_count,s5_count=s5_count,s6_count=s6_count,s7_count=s7_count)


    if subject_count == 7:
        s1_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[0]})
        s1 = pandas.Series(s1_cursor)
        s1.to_dict()
        s1_count = s1.count()
        
        s2_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[1]})
        s2 = pandas.Series(s2_cursor)
        s2.to_dict()
        s2_count = s2.count()
        
        s3_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[2]})
        s3 = pandas.Series(s3_cursor)
        s3.to_dict()
        s3_count = s3.count()
        
        s4_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[3]})
        s4 = pandas.Series(s4_cursor)
        s4.to_dict()
        s4_count = s4.count()
        
        s5_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[4]})
        s5 = pandas.Series(s5_cursor)
        s5.to_dict()
        s5_count = s5.count()
        
        s6_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[5]})
        s6 = pandas.Series(s6_cursor)
        s6.to_dict()
        s6_count = s6.count()
        
        s7_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[6]})
        s7 = pandas.Series(s7_cursor)
        s7.to_dict()
        s7_count = s7.count()
        
        s8_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[7]})
        s8 = pandas.Series(s8_cursor)
        s8.to_dict()
        s8_count = s8.count()
        marks = db.collection.find()     
        return render_template("charts.html",distinction=distinction,subject_count=subject_count,subjects=subjects,count_distinction=count_distinction,count_first_class=count_first_class,count_second_class=count_second_class,count_fail=count_fail,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s1_count=s1_count,s2_count=s2_count,s3_count=s3_count,s4_count=s4_count,s5_count=s5_count,s6_count=s6_count,s7_count=s7_count,s8_count=s8_count)

    if subject_count == 8:
        s1_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[0]})
        s1 = pandas.Series(s1_cursor)
        s1.to_dict()
        s1_count = s1.count()
        
        s2_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[1]})
        s2 = pandas.Series(s2_cursor)
        s2.to_dict()
        s2_count = s2.count()
        
        s3_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[2]})
        s3 = pandas.Series(s3_cursor)
        s3.to_dict()
        s3_count = s3.count()
        
        s4_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[3]})
        s4 = pandas.Series(s4_cursor)
        s4.to_dict()
        s4_count = s4.count()
        
        s5_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[4]})
        s5 = pandas.Series(s5_cursor)
        s5.to_dict()
        s5_count = s5.count()
        
        s6_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[5]})
        s6 = pandas.Series(s6_cursor)
        s6.to_dict()
        s6_count = s6.count()
        
        s7_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[6]})
        s7 = pandas.Series(s7_cursor)
        s7.to_dict()
        s7_count = s7.count()
        
        s8_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[7]})
        s8 = pandas.Series(s8_cursor)
        s8.to_dict()
        s8_count = s8.count()
        
        s9_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[8]})
        s9 = pandas.Series(s9_cursor)
        s9.to_dict()
        s9_count = s9.count()
        marks = db.collection.find()      
        return render_template("charts.html",subject_count=subject_count,subjects=subjects,count_distinction=count_distinction,count_first_class=count_first_class,count_second_class=count_second_class,count_fail=count_fail,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s9=s9,s1_count=s1_count,s2_count=s2_count,s3_count=s3_count,s4_count=s4_count,s5_count=s5_count,s6_count=s6_count,s7_count=s7_count,s8_count=s8_count,s9_count=s9_count)

    if subject_count == 9:
        s1_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[0]})
        s1 = pandas.Series(s1_cursor)
        s1.to_dict()
        s1_count = s1.count()
        
        s2_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[1]})
        s2 = pandas.Series(s2_cursor)
        s2.to_dict()
        s2_count = s2.count()
        
        s3_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[2]})
        s3 = pandas.Series(s3_cursor)
        s3.to_dict()
        s3_count = s3.count()
        
        s4_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[3]})
        s4 = pandas.Series(s4_cursor)
        s4.to_dict()
        s4_count = s4.count()
        
        s5_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[4]})
        s5 = pandas.Series(s5_cursor)
        s5.to_dict()
        s5_count = s5.count()
        
        s6_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[5]})
        s6 = pandas.Series(s6_cursor)
        s6.to_dict()
        s6_count = s6.count()
        
        s7_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[6]})
        s7 = pandas.Series(s7_cursor)
        s7.to_dict()
        s7_count = s7.count()
        
        s8_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[7]})
        s8 = pandas.Series(s8_cursor)
        s8.to_dict()
        s8_count = s8.count()
        
        s9_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[8]})
        s9 = pandas.Series(s9_cursor)
        s9.to_dict()
        s9_count = s9.count()
        
        s10_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[9]})
        s10 = pandas.Series(s10_cursor)
        s10.to_dict()
        s10_count = s10.count()
        marks = db.collection.find()      
        return render_template("charts.html",subject_count=subject_count,subjects=subjects,count_distinction=count_distinction,count_first_class=count_first_class,count_second_class=count_second_class,count_fail=count_fail,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s9=s9,s10=s10,s1_count=s1_count,s2_count=s2_count,s3_count=s3_count,s4_count=s4_count,s5_count=s5_count,s6_count=s6_count,s7_count=s7_count,s8_count=s8_count,s9_count=s9_count,s10_count=s10_count)

    if subject_count == 10:
        s1_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[0]})
        s1 = pandas.Series(s1_cursor)
        s1.to_dict()
        s1_count = s1.count()
        
        s2_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[1]})
        s2 = pandas.Series(s2_cursor)
        s2.to_dict()
        s2_count = s2.count()
        
        s3_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[2]})
        s3 = pandas.Series(s3_cursor)
        s3.to_dict()
        s3_count = s3.count()
        
        s4_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[3]})
        s4 = pandas.Series(s4_cursor)
        s4.to_dict()
        s4_count = s4.count()
        
        s5_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[4]})
        s5 = pandas.Series(s5_cursor)
        s5.to_dict()
        s5_count = s5.count()
        
        s6_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[5]})
        s6 = pandas.Series(s6_cursor)
        s6.to_dict()
        s6_count = s6.count()
        
        s7_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[6]})
        s7 = pandas.Series(s7_cursor)
        s7.to_dict()
        s7_count = s7.count()
        
        s8_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[7]})
        s8 = pandas.Series(s8_cursor)
        s8.to_dict()
        s8_count = s8.count()
        
        s9_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[8]})
        s9 = pandas.Series(s9_cursor)
        s9.to_dict()
        s9_count = s9.count()
        
        s10_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[9]})
        s10 = pandas.Series(s10_cursor)
        s10.to_dict()
        s10_count = s10.count()
        
        s11_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[10]})
        s11 = pandas.Series(s11_cursor)
        s11.to_dict()
        s11_count = s11.count()
        marks = db.collection.find()       
        return render_template("charts.html",marks=marks,subject_count=subject_count,subjects=subjects,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s9=s9,s10=s10,s11=s11,s1_count=s1_count,s2_count=s2_count,s3_count=s3_count,s4_count=s4_count,s5_count=s5_count,s6_count=s6_count,s7_count=s7_count,s8_count=s8_count,s9_count=s9_count,s10_count=s10_count,s11_count=s11_count)

    if subject_count == 11:
        s1_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[0]})
        s1 = pandas.Series(s1_cursor)
        s1.to_dict()
        s1_count = s1.count()
        
        s2_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[1]})
        s2 = pandas.Series(s2_cursor)
        s2.to_dict()
        s2_count = s2.count()
        
        s3_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[2]})
        s3 = pandas.Series(s3_cursor)
        s3.to_dict()
        s3_count = s3.count()
        
        s4_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[3]})
        s4 = pandas.Series(s4_cursor)
        s4.to_dict()
        s4_count = s4.count()
        
        s5_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[4]})
        s5 = pandas.Series(s5_cursor)
        s5.to_dict()
        s5_count = s5.count()
        
        s6_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[5]})
        s6 = pandas.Series(s6_cursor)
        s6.to_dict()
        s6_count = s6.count()
        
        s7_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[6]})
        s7 = pandas.Series(s7_cursor)
        s7.to_dict()
        s7_count = s7.count()
        
        s8_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[7]})
        s8 = pandas.Series(s8_cursor)
        s8.to_dict()
        s8_count = s8.count()
        
        s9_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[8]})
        s9 = pandas.Series(s9_cursor)
        s9.to_dict()
        s9_count = s9.count()
        
        s10_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[9]})
        s10 = pandas.Series(s10_cursor)
        s10.to_dict()
        s10_count = s10.count()
        
        s11_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[10]})
        s11 = pandas.Series(s11_cursor)
        s11.to_dict()
        s11_count = s11.count()
        
        s12_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[11]})
        s12 = pandas.Series(s12_cursor)
        s12.to_dict()
        s12_count = s12.count()
        marks = db.collection.find()       
        return render_template("charts.html",subject_count=subject_count,subjects=subjects,count_distinction=count_distinction,count_first_class=count_first_class,count_second_class=count_second_class,count_fail=count_fail,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s9=s9,s10=s10,s11=s11,s12=s12,s1_count=s1_count,s2_count=s2_count,s3_count=s3_count,s4_count=s4_count,s5_count=s5_count,s6_count=s6_count,s7_count=s7_count,s8_count=s8_count,s9_count=s9_count,s10_count=s10_count,s11_count=s11_count,s12_count=s12_count)

    if subject_count == 12:
        s1_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[0]})
        s1 = pandas.Series(s1_cursor)
        s1.to_dict()
        s1_count = s1.count()
        
        s2_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[1]})
        s2 = pandas.Series(s2_cursor)
        s2.to_dict()
        s2_count = s2.count()
        
        s3_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[2]})
        s3 = pandas.Series(s3_cursor)
        s3.to_dict()
        s3_count = s3.count()
        
        s4_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[3]})
        s4 = pandas.Series(s4_cursor)
        s4.to_dict()
        s4_count = s4.count()
        
        s5_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[4]})
        s5 = pandas.Series(s5_cursor)
        s5.to_dict()
        s5_count = s5.count()
        
        s6_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[5]})
        s6 = pandas.Series(s6_cursor)
        s6.to_dict()
        s6_count = s6.count()
        
        s7_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[6]})
        s7 = pandas.Series(s7_cursor)
        s7.to_dict()
        s7_count = s7.count()
        
        s8_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[7]})
        s8 = pandas.Series(s8_cursor)
        s8.to_dict()
        s8_count = s8.count()
        
        s9_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[8]})
        s9 = pandas.Series(s9_cursor)
        s9.to_dict()
        s9_count = s9.count()
        
        s10_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[9]})
        s10 = pandas.Series(s10_cursor)
        s10.to_dict()
        s10_count = s10.count()
        
        s11_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[10]})
        s11 = pandas.Series(s11_cursor)
        s11.to_dict()
        s11_count = s11.count()
        
        s12_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[11]})
        s12 = pandas.Series(s12_cursor)
        s12.to_dict()
        s12_count = s12.count()
        marks = db.collection.find()       
        return render_template("charts.html",subject_count=subject_count,subjects=subjects,count_distinction=count_distinction,count_first_class=count_first_class,count_second_class=count_second_class,count_fail=count_fail,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s9=s9,s10=s10,s11=s11,s12=s12,s1_count=s1_count,s2_count=s2_count,s3_count=s3_count,s4_count=s4_count,s5_count=s5_count,s6_count=s6_count,s7_count=s7_count,s8_count=s8_count,s9_count=s9_count,s10_count=s10_count,s11_count=s11_count,s12_count=s12_count)

    if subject_count == 13:
        s1_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[0]})
        s1 = pandas.Series(s1_cursor)
        s1.to_dict()
        s1_count = s1.count()
        
        s2_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[1]})
        s2 = pandas.Series(s2_cursor)
        s2.to_dict()
        s2_count = s2.count()
        
        s3_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[2]})
        s3 = pandas.Series(s3_cursor)
        s3.to_dict()
        s3_count = s3.count()
        
        s4_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[3]})
        s4 = pandas.Series(s4_cursor)
        s4.to_dict()
        s4_count = s4.count()
        
        s5_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[4]})
        s5 = pandas.Series(s5_cursor)
        s5.to_dict()
        s5_count = s5.count()
        
        s6_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[5]})
        s6 = pandas.Series(s6_cursor)
        s6.to_dict()
        s6_count = s6.count()
        
        s7_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[6]})
        s7 = pandas.Series(s7_cursor)
        s7.to_dict()
        s7_count = s7.count()
        
        s8_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[7]})
        s8 = pandas.Series(s8_cursor)
        s8.to_dict()
        s8_count = s8.count()
        
        s9_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[8]})
        s9 = pandas.Series(s9_cursor)
        s9.to_dict()
        s9_count = s9.count()
        
        s10_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[9]})
        s10 = pandas.Series(s10_cursor)
        s10.to_dict()
        s10_count = s10.count()
        
        s11_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[10]})
        s11 = pandas.Series(s11_cursor)
        s11.to_dict()
        s11_count = s11.count()
        
        s13_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[12]})
        s13 = pandas.Series(s13_cursor)
        s13.to_dict()
        s13_count = s13.count()
        marks = db.collection.find()       
        return render_template("charts.html",marks=marks,subject_count=subject_count,subjects=subjects,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s9=s9,s10=s10,s11=s11,s12=s12,s13=s13,s1_count=s1_count,s2_count=s2_count,s3_count=s3_count,s4_count=s4_count,s5_count=s5_count,s6_count=s6_count,s7_count=s7_count,s8_count=s8_count,s9_count=s9_count,s10_count=s10_count,s11_count=s11_count,s12_count=s12_count,s13_count=s13_count)

    if subject_count == 14:
        s1_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[0]})
        s1 = pandas.Series(s1_cursor)
        s1.to_dict()
        s1_count = s1.count()
        
        s2_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[1]})
        s2 = pandas.Series(s2_cursor)
        s2.to_dict()
        s2_count = s2.count()
        
        s3_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[2]})
        s3 = pandas.Series(s3_cursor)
        s3.to_dict()
        s3_count = s3.count()
        
        s4_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[3]})
        s4 = pandas.Series(s4_cursor)
        s4.to_dict()
        s4_count = s4.count()
        
        s5_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[4]})
        s5 = pandas.Series(s5_cursor)
        s5.to_dict()
        s5_count = s5.count()
        
        s6_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[5]})
        s6 = pandas.Series(s6_cursor)
        s6.to_dict()
        s6_count = s6.count()
        
        s7_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[6]})
        s7 = pandas.Series(s7_cursor)
        s7.to_dict()
        s7_count = s7.count()
        
        s8_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[7]})
        s8 = pandas.Series(s8_cursor)
        s8.to_dict()
        s8_count = s8.count()
        
        s9_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[8]})
        s9 = pandas.Series(s9_cursor)
        s9.to_dict()
        s9_count = s9.count()
        
        s10_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[9]})
        s10 = pandas.Series(s10_cursor)
        s10.to_dict()
        s10_count = s10.count()
        
        s11_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[10]})
        s11 = pandas.Series(s11_cursor)
        s11.to_dict()
        s11_count = s11.count()
        
        s13_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[12]})
        s13 = pandas.Series(s13_cursor)
        s13.to_dict()
        s13_count = s13.count()
        
        s14_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[13]})
        s14 = pandas.Series(s14_cursor)
        s14.to_dict()
        s14_count = s14.count()
        marks = db.collection.find()        
        return render_template("charts.html",subject_count=subject_count,subjects=subjects,count_distinction=count_distinction,count_first_class=count_first_class,count_second_class=count_second_class,count_fail=count_fail,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s9=s9,s10=s10,s11=s11,s12=s12,s13=s13,s14=s14,s1_count=s1_count,s2_count=s2_count,s3_count=s3_count,s4_count=s4_count,s5_count=s5_count,s6_count=s6_count,s7_count=s7_count,s8_count=s8_count,s9_count=s9_count,s10_count=s10_count,s11_count=s11_count,s12_count=s12_count,s13_count=s13_count,s14_count=s14_count)

    if subject_count == 15:
        s1_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[0]})
        s1 = pandas.Series(s1_cursor)
        s1.to_dict()
        s1_count = s1.count()
        
        s2_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[1]})
        s2 = pandas.Series(s2_cursor)
        s2.to_dict()
        s2_count = s2.count()
        
        s3_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[2]})
        s3 = pandas.Series(s3_cursor)
        s3.to_dict()
        s3_count = s3.count()
        
        s4_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[3]})
        s4 = pandas.Series(s4_cursor)
        s4.to_dict()
        s4_count = s4.count()
        
        s5_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[4]})
        s5 = pandas.Series(s5_cursor)
        s5.to_dict()
        s5_count = s5.count()
        
        s6_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[5]})
        s6 = pandas.Series(s6_cursor)
        s6.to_dict()
        s6_count = s6.count()
        
        s7_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[6]})
        s7 = pandas.Series(s7_cursor)
        s7.to_dict()
        s7_count = s7.count()
        
        s8_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[7]})
        s8 = pandas.Series(s8_cursor)
        s8.to_dict()
        s8_count = s8.count()
        
        s9_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[8]})
        s9 = pandas.Series(s9_cursor)
        s9.to_dict()
        s9_count = s9.count()
        
        s10_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[9]})
        s10 = pandas.Series(s10_cursor)
        s10.to_dict()
        s10_count = s10.count()
        
        s11_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[10]})
        s11 = pandas.Series(s11_cursor)
        s11.to_dict()
        s11_count = s11.count()
        
        s13_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[12]})
        s13 = pandas.Series(s13_cursor)
        s13.to_dict()
        s13_count = s13.count()
        
        s14_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[13]})
        s14 = pandas.Series(s14_cursor)
        s14.to_dict()
        s14_count = s14.count()
        
        s15_cursor = db.collection.find(
        {"sem": semister, "mse": mse, "year": year, "subject": subjects[15]})
        s15 = pandas.Series(s15_cursor)
        s15.to_dict()
        s15_count = s15.count()
        marks = db.collection.find()        
        return render_template("charts.html",subject_count=subject_count,subjects=subjects,count_distinction=count_distinction,count_first_class=count_first_class,count_second_class=count_second_class,count_fail=count_fail,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s9=s9,s10=s10,s11=s11,s12=s12,s13=s13,s14=s14,s15=s15,s1_count=s1_count,s2_count=s2_count,s3_count=s3_count,s4_count=s4_count,s5_count=s5_count,s6_count=s6_count,s7_count=s7_count,s8_count=s8_count,s9_count=s9_count,s10_count=s10_count,s11_count=s11_count,s12_count=s12_count,s13_count=s13_count,s14_count=s14_count,s15_count=s15_count)

        





    ############## Subject1 #####################
    if subjects:
        s1_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[0]})
        s1 = pandas.Series(s1_cursor)
        s1.to_dict()
        s1_count = s1.count()
        ################## Subject2 ################
        s2_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[1]})
        s2 = pandas.Series(s2_cursor)
        s2.to_dict()
        s2_count = s2.count()
        ##################### Subject3 ###############
        s3_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[2]})
        s3 = pandas.Series(s3_cursor)
        s3.to_dict()
        s3_count = s3.count()

        #################### Subject4 #################
        
        s4_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[3]})
        s4 = pandas.Series(s4_cursor)
        s4.to_dict()
        s4_count = s4.count()

        #################### Subject5 #################
        s5_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[4]})
        s5 = pandas.Series(s5_cursor)
        s5.to_dict()
        s5_count = s5.count()
        #################### Subject6 #################
        s6_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[5]})
        s6 = pandas.Series(s6_cursor)
        s6.to_dict()
        s6_count = s6.count()
        ######################## Subject7 ###############
        
        s7_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[6]})
        s7 = pandas.Series(s7_cursor)
        s7.to_dict()
        s7_count = s7.count()
        ##################### Subject8 #################
        s7_cursor = db.collection.find(
            {"sem": semister, "mse": mse, "year": year, "subject": subjects[7]})
        s8 = pandas.Series(s7_cursor)
        s8.to_dict()
        s8_count = s8.count()
        return render_template("chart.html", s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7, s8=s8, s1_count=s1_count, s2_count=s2_count, s3_count=s3_count, s4_count=s4_count, s5_count=s5_count, s6_count=s6_count, s7_count=s7_count, s8_count=s8_count, subjects=subjects)
    return "Empty"




        # for output in db.fs.files.find({"filename":image_file,"semister":semister,"mse":mse}):
        #     output = fs.get(stored).read()
        #     outputfilename = image_file
        #     print(output)
        #     outputfile = open(outputfilename,"wb")
        #     result = outputfile.write(output)
        #     filename = "output.jpg"

    return render_template("image_export.html", image_file=image_file)


#     return '''
#     <p> Successfully uploaded to database </p>
#     <form action="upload_image">
#     <input type="submit" value="Redirect">
#     <img src="{{nmit.png}}">
#     </form>
# '''

    # print (image_path)
    # with open(image_path, "rb") as imagefile:
    #     encode = base64.b64encode(imagefile.read())
    #     b = fs.put(encode)

    #     for retrieve in db.fs.chunks.find():
    #         decoder = json.dumps(base64.b64decode(retrieve))
    #         export = fs.get(decoder)
    #         data = pandas.DataFrame({export},index[0])
    #         writejson = data.to_json("image_data.json")
    #         with open(writejson,"rb") as imagefile:
    #             decode = base64.b64decode(imagefile)
    #             c = fs.get(decode)
    #             print(c)
    #     return render_template("success.html")

    #         # imgdata = base64.b64decode(i)
    #         # filename = 'output.png'
    #         # with open(filename,'w') as imgfile:
    #         #     x = imagefile.write(imgdata)
    #         # out = fs.get(i)
    #         # b = out.filename
    #         # print(out)
    #         # with open(i,'wb') as imagefile:
    # #         #     b = imagefile.write(imagefile.decodebytes('base64'))
    # # with open("123.png","wb") as imgfile:
    # #     for i in db.fs.chunks.find():
    # #         print(i)
    # #         decode = base64.b64decode(i)
    # #         fs.get(decode)


######################################################### End Of Image Upload section #######################################################


@app.route("/internal")
def papers():
    return render_template("internal_paper.html")


@app.route("/download_paper", methods=['POST'])
def download():
    # '''
    # <input type="number" name="sem">
    # <input type="number" name="mse">
    # '''
    semister = request.form['semister']
    mse = request.form['mse']

    for database in db.fs.files.find({"semister": semister, "mse": mse}):
        print(database)
    return "Success brooo"


#############################################################################Excel Upload Part ####################################################

@app.route("/success", methods=['POST'])
def success():
    csvfilepath = request.form["file"]
    print(csvfilepath)

    with open(csvfilepath, "r") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for csvrow in csvreader:
            print(csvrow)
            # USN = csvrow["USN"]
            # data[USN] = csvrow
            db.collection.insert_one(csvrow)

    # with open(jsonfilepath,"w") as jsonfile:
    #     jsonfile.write(data)

    # allresult = db.collection.insert_one(template_dct)
    # print('Inserted post id %s ' % allresult.inserted_id)

    return render_template("Success.html", csvfilepath=csvfilepath)

############################################################################### End Excel upload part ############################################


################################################################################ Student details ##############################################
@app.route("/download", methods=['POST', 'GET'])
def students():
    return render_template("download.html")


@app.route("/result", methods=['GET', 'POST'])
def results():
    semister = request.form['sem']
    mse = request.form['mse']
    year = request.form['year']
    # finaldictlist = []
    # middlelist = []
    cursor = db.collection.find({"sem": semister, "mse": mse, "year": year})
    x = pandas.Series(cursor)
    x.to_dict()
    # finaldictlist = finaldictlist.append(database)
    # data = pandas.DataFrame()
    # stringdata = data.to_dict()
    # middlelist = database.items()
    # datas = [database]

    #     middlelist = [(k,v) for k,v in database.items()]
    #     finaldictlist.append(middlelist)
    # print(finaldictlist)
    return render_template("student.html", database=x, semister=semister, mse=mse, year=year)




@app.errorhandler(404)
def page_not_found(error):
    return "requested Page is not found"


@app.route("/result/exported", methods=['POST'])
def export():
    semister = request.form['sem']
    mse = request.form['mse']
    year = request.form['year']
    cursor = db.collection.find({"sem": semister, "mse": mse, "year": year})
    x = pandas.DataFrame(list(cursor))
    x.to_csv("C:/Users/darsh/Downloads/result.csv")
    return render_template("export_template.html")

# @app.route("/result/charts",methods=['POST','GET'])
# def charts():
#     sem = 6
#     year = 2020
#     secursor = db.collection.find({"sem":"6","year":"2020","subject":"SE"})
#     se = pandas.Series(secursor)
#     se.to_dict()
#     print(se)
#     return render_template("chart.html",se=se)




################################################################################# End Student details ###############################################

@app.route("/output", methods=['GET', 'POST'])
def output():
    cursor = db.collection.find()
    x = pandas.DataFrame(list(cursor))
    print(x)
    x.to_csv("templates/output.csv")
    # Refering website https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html#pandas.DataFrame.to_excel
    x.to_html("templates/output.html")

    return render_template("output.html")


myclient.close()

if __name__ == "__main__":
    app.debug = True
    app.run(port=3000)
