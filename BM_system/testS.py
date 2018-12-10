from flask import Flask, render_template, request, Response

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'hell'

@app.route('/test/<temp_user_key>', methods=['GET', 'POST'])
def sign_up(temp_user_key):
    data =temp_user_key.split('&')

    return "_".join(data)

if __name__ == '__main__':
    app.run()