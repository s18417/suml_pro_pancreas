import os.path
import pickle
import sys

import sklearn
import imblearn
from flask import Flask, redirect, render_template, request, url_for, send_file, send_from_directory, current_app

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def main_page():
    filename = "best_rfc.sv"
    model = pickle.load(open(filename, 'rb'))
    dataF = open("dane.csv", "r")
    lines = dataF.readlines()
    separated_lines = []
    count = 1
    for line in lines:
        separated_lines.append(line.split(","))
        count += 1

    if request.method == "POST":
        data = [[
            request.form["age"],
            request.form["cohort"],
            request.form["plasma_CA19"],
            request.form["creatitine"],
            request.form["LYVE1"],
            request.form["REG1B"],
            request.form["TFF1"],
            request.form["REG1A"],
        ]]
        res = model.predict(data)

        if res[0] == 1.:
            res = "control"
        elif res[0] == 2.:
            res = "benign hepatobiliary disease"
        else:
            res = "pancreatic cancer"
        data += [
            res
        ]
        if data[0][1] == "0":
            data[0][1] = "female"
        elif data[0][1] == "1":
            data[0][1] = "male"
        with open("dane.csv", "a") as dane:
            dane.write(data.__str__().replace("[", "").replace("]", "").replace("'", "") + "\n")
        return redirect(url_for("main_page", lines=separated_lines))
    else:
        return render_template("form.html", lines=separated_lines)


@app.route('/download')
def downloadFile ():

    path = app.root_path+"/dane.csv"
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
