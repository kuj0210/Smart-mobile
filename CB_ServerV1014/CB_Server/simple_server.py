from flask import Flask, render_template, request, Response
import Register
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hell'

@app.route('/<temp_user_key>', methods=['GET', 'POST'])
def sign_up(temp_user_key):
    if request.method == 'GET':
        return render_template('regist.html')

    else :
        serial = request.form['serial']
        print(serial, temp_user_key)
        reg = Register()
        reg.insertUserData(temp_user_key, serial)
        return render_template("regist_success.html"), 200

if __name__ == '__main__':
    app.run()