from flask import Flask, redirect, url_for, request
import os
app = Flask(__name__)


@app.route('/naumen',methods = ['POST', 'GET'])
def login():
   file_path = "hosts"
   if request.method == 'POST':
      user = request.form['hosts']
      with open(file_path ,'w') as hosts_file:
          hosts_file.write(user)
      os.system("/usr/bin/python3 /home/userDocuments/dev/naumen/main.py -c '/home/yser/Documents/dev/naumen/config'  --hosts {} --message {}".format(file_path,"/home/user/Documents/dev/naumen/message"))
      return  os.path.abspath(file_path)

if __name__ == '__main__':
   app.run(debug = True)
