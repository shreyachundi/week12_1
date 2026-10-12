from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    student_id = request.form['student_id']

    return render_template(
        'success.html',
        name=name,
        email=email,
        student_id=student_id
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)