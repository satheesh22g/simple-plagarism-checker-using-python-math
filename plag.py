
from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
from werkzeug import secure_filename
import docx2txt
import os
import PyPDF2
import re
import math
app = Flask(__name__)
@app.route("/")
def index():
	return render_template('index.html')
@app.route("/upload")
def loadPage():
	return render_template('upload.html')
@app.route("/upload", methods=['GET','POST'])
def pragarism():
    try:
        if request.method == 'POST':
            file1 = request.files['file']
            filename = secure_filename(file1.filename)
            ext = os.path.splitext(filename)[-1].lower()
            if ext == ".docx":
                inputQuery = docx2txt.process(filename)
            elif ext == ".txt":
                inputQuery = open(filename,"r")
            else:
                output = "is an unknown file format."
                return render_template('upload.html', output=output)
    except (FileNotFoundError, IOError):
        return "no file is selected"
    fd = open("database1.txt", "r+")
    universalSetOfUniqueWords = []
    matchPercentage = 0
    lowercaseQuery = ""
    for line in inputQuery:
        lowercaseQuery += line.lower()
    if lowercaseQuery=="":
        output="Document is empty"
        return render_template('upload.html', output=output)
    queryWordList = re.sub("[^\w]", " ",lowercaseQuery).split()
    for word in queryWordList:
        if word not in universalSetOfUniqueWords:
            universalSetOfUniqueWords.append(word)
    database1 = fd.read().lower()
    databaseWordList = re.sub("[^\w]", " ",database1).split()
    for word in databaseWordList:
        if word not in universalSetOfUniqueWords:
            universalSetOfUniqueWords.append(word)    
    queryTF = []
    databaseTF = []
    for word in universalSetOfUniqueWords:
        queryTfCounter = 0
        databaseTfCounter = 0

        for word2 in queryWordList:
            if word == word2:
                queryTfCounter += 1
        queryTF.append(queryTfCounter)
        for word2 in databaseWordList:
            if word == word2:
                databaseTfCounter += 1
        databaseTF.append(databaseTfCounter)
    dotProduct = 0
    for i in range (len(queryTF)):
        dotProduct += queryTF[i]*databaseTF[i]
    queryVectorMagnitude = 0
    for i in range (len(queryTF)):
        queryVectorMagnitude += queryTF[i]**2
    queryVectorMagnitude = math.sqrt(queryVectorMagnitude)
    databaseVectorMagnitude = 0
    for i in range (len(databaseTF)):
        databaseVectorMagnitude += databaseTF[i]**2
    databaseVectorMagnitude = math.sqrt(databaseVectorMagnitude)
    matchPercentage = (float)(dotProduct / (queryVectorMagnitude * databaseVectorMagnitude))*100
    if matchPercentage<60:
        fd.write(lowercaseQuery)
        output="Your Submission is Accepted. Your assignment matches  %0.02f%% with database."%matchPercentage
    else:
        output = "Your Submission is Rejected. Only less than 60 percentage match only considered, %0.02f%% with database."%matchPercentage
    return render_template('upload.html', output=output)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)