from flask import Flask, flash, jsonify, redirect, request
import os

from usecase import generatePaymentDetail


app = Flask(__name__)


@app.route('/')
def home():
    return "Api to match procces invoices"


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
         # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist("file")
        return generatePaymentDetail(files)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
