import os.path
import pickle
import sys

import sklearn
import imblearn
from flask import Flask, redirect, render_template, request, url_for, send_file, send_from_directory, current_app

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def hello_world():
    filename = "grid_imba8.sv"
    model = pickle.load(open(filename, 'rb'))
    dataF = open("dane.csv", "r")
    lines = dataF.readlines()
    separated_lines = []
    count = 1
    for line in lines:
        separated_lines.append(line.split(","))
        count += 1
    # print(separated_lines)
    # print(separated_lines[0])

    if request.method == "POST":
        data = [[
            request.form["cohort"],
            request.form["sample_origin"],
            request.form["age"],
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
        print(data[0][1])
        print(data)
        if data[0][1] == "1":
            data[0][1] = "BPTB"
        elif data[0][1] == "2":
            data[0][1] = "LIV"
        elif data[0][1] == "3":
            data[0][1] = "ESP"
        else:
            data[0][1] = "UCL"
        print(data)
        with open("dane.csv", "a") as dane:
            dane.write(data.__str__().replace("[", "").replace("]", "").replace("'", "") + "\n")
        return redirect(url_for("hello_world", lines=separated_lines))
        # return render_template("form.html",lines=separated_lines)
    else:
        # return redirect(url_for("hello_world", lines=separated_lines))
        return render_template("form.html", lines=separated_lines)


@app.route('/download')
def downloadFile ():

    path = app.root_path+"/dane.csv"
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
