from flask import Flask, request, render_template_string, jsonify
import subprocess
import os
import sqlite3
import requests
from lxml import etree

aws_access_key_id = 'AKIA2JAPX77RGLB664VE'
aws_secret = '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'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    db = sqlite3.connect("tutorial.db")
    cursor = db.cursor()
    username = ''
    password = ''
    try:
        cursor.execute("SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password))
    except:
        pass

    if request.method == 'POST':
        if 'command' in request.form:
            cmd = request.form['command']
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                output = stdout.decode('utf-8')
            else:
                output = f"Error (Exit Code: {process.returncode}):\n{stderr.decode('utf-8')}"

        elif 'file' in request.files:
            uploaded_file = request.files['file']
            uploaded_file.save(os.path.join('/uploads', uploaded_file.filename))
            output = f"File {uploaded_file.filename} uploaded successfully!"

        elif 'sql' in request.form:
            sql = request.form['sql']
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
                if rows:
                    output = "Results:\n" + "\n".join(str(row) for row in rows)
                else:
                    output = "Query executed successfully, but no results found."
            except Exception as e:
                output = f"SQL Error: {e}"

        elif 'xss' in request.form:
            xss_input = request.form['xss']
            output = f"Reflected XSS result: {xss_input}"

        elif 'xml' in request.form:
            xml_data = request.form['xml']
            try:
                parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
                tree = etree.fromstring(xml_data.encode(), parser)
                output = f"Parsed XML: {etree.tostring(tree, encoding='unicode')}"
            except Exception as e:
                output = f"XML Parsing Error: {e}"

        elif 'url' in request.form:
            url = request.form['url']
            try:
                response = requests.get(url)
                output = f"SSRF Response: {response.text[:200]}"
            except Exception as e:
                output = f"SSRF Error: {e}"

        if 'username' in request.form:
            username = request.form['username']
            try:
                query = "SELECT password FROM users WHERE username = '{}'".format(username)
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    output = f"Password for {username}: {result[0]}"
                else:
                    output = "User not found."
            except Exception as e:
                output = f"SQL Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)