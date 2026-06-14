import os
import psycopg2
from flask import *

app=Flask(__name__)

# Database Configuration
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
    )

try:
    db = get_db_connection()
    print("Database connected successfully")
except Exception as e:
    print("Database Error:", e)


@app.route("/")
def openhomepage():
    name = 'Karmegam'
    return render_template("index.html",name = name)

@app.route("/addstudent")
def studentregister():
    return render_template('studentregister.html')
@app.route('/savetodbstudent', methods=['GET', 'POST'])
def add_student():
    print("i am here")
    if request.method == 'POST':
        print("clicked")

        first_name = request.form['fname']
        last_name = request.form['lname']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        course = request.form['course']
        hobbies = ",".join(request.form.getlist('hobbies'))
        print(first_name,
            last_name,
            dob,
            gender,
            email,
            phone,
            address,
            course,
            hobbies
)

        db = get_db_connection()
        cursor = db.cursor() # excute the query

        sql = """
        INSERT INTO student_registration
        (
            first_name,
            last_name,
            date_of_birth,
            gender,
            email,
            phone_number,
            address,
            course,
            hobbies
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            first_name,
            last_name,
            dob,
            gender,
            email,
            phone,
            address,
            course,
            hobbies
        )

        cursor.execute(sql, values)
        db.commit()

        return render_template('index.html')

    return render_template('studentregister.html')

@app.route("/viewstudents")
def view_students():
    db = get_db_connection()
    cursor = db.cursor()

    sql = """
    SELECT
        student_id,
        first_name,
        last_name,
        date_of_birth,
        gender,
        email,
        phone_number,
        address,
        course,
        hobbies,
        registration_date
    FROM student_registration
    """

    cursor.execute(sql)

    students = cursor.fetchall()

    cursor.close()

    return render_template(
        "viewstudents.html",
        students=students
    )

@app.route("/editstudent/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    db = get_db_connection()
    cursor = db.cursor()

    if request.method == "POST":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]
        course = request.form["course"]
        hobbies = ",".join(request.form.getlist("hobbies"))

        sql = """
        UPDATE student_registration
        SET
            first_name=%s,
            last_name=%s,
            date_of_birth=%s,
            gender=%s,
            email=%s,
            phone_number=%s,
            address=%s,
            course=%s,
            hobbies=%s
        WHERE student_id=%s
        """

        values = (
            first_name,
            last_name,
            dob,
            gender,
            email,
            phone,
            address,
            course,
            hobbies,
            id
        )

        cursor.execute(sql, values)

        db.commit()

        cursor.close()

        return redirect("/viewstudents")


    sql = """
    SELECT
        student_id,
        first_name,
        last_name,
        date_of_birth,
        gender,
        email,
        phone_number,
        address,
        course,
        hobbies
    FROM student_registration
    WHERE student_id=%s
    """

    cursor.execute(sql, (id,))

    student = cursor.fetchone()

    cursor.close()

    return render_template(
        "editstudent.html",
        student=student
    )

@app.route("/deletestudent/<int:id>")
def delete_student(id):
    db = get_db_connection()
    cursor = db.cursor()

    sql = """
    DELETE FROM student_registration
    WHERE student_id=%s
    """

    cursor.execute(sql, (id,))

    db.commit()

    cursor.close()

    return redirect("/")

if __name__=='__main__':
    app.run(debug=True)