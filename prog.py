from flask import Flask, url_for, render_template, jsonify, request, make_response, redirect
import os, pipes, subprocess

app = Flask(__name__)

@app.route("/")
def hello():
  return render_template("hello.html")

@app.route('/start_prog', methods=['POST'])
def start_prog():
    pname = request.form['pname']
    open('./data/' + pname + '.c', 'a').close()
    resp = make_response(redirect(url_for('prog')))
    resp.set_cookie('fname', pname)
    return resp

@app.route("/prog")
def prog():
  return render_template("prog.html", fname=request.cookies.get('fname'))

@app.route('/files', methods=['GET','POST'])
def load_file():
  fname = request.cookies.get('fname')
  fpath = './data/' + fname + '.c';
  if fname and os.path.exists(fpath):
    if (request.method == 'GET'):
      with open(fpath, 'r') as f:
        file_out = f.read()
      return file_out
    elif (request.method == 'POST' and 'file' in request.form):
      with open(fpath, 'w') as f:
        f.write(request.form['file'])
      return "Ok"
  else:
    abort(404)
    return "Fail: No File"

@app.route('/get/<fname>')
def get_file(fname):
  fpath = './data/' + fname;
  with open(fpath, 'r') as f:
    file_code = f.read()
  return render_template("code_show.html", code=file_code)

@app.route('/list')
def get_flist():
  return render_template("list_files.html", files=os.listdir('./data'))

@app.route('/compile')
def compile():
  fbase = '/home/iain/py-interp/'
  fname = request.cookies.get('fname')
  p = subprocess.Popen(['gcc','./data/' + fname + '.c','-o','./data/prog/' +fname],
          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
          cwd=fbase)
  output = {}
  output['stdout'], output['stderr']= p.communicate()
  if (p.returncode == 0):
    chp = subprocess.Popen(['./runner.py', fname],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output['chstdout'], output['chstderr'] = chp.communicate()
  return jsonify(output)

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)
