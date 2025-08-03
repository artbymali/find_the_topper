from flask import Flask, request, render_template
from highest_marks_finder import find_topper

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def get_data():
    students = None
    marks = None

    if request.method == "POST":
        dept = request.form.get("dept").upper()
        year = request.form.get("year")
        semester = request.form.get("semester")
        batch = request.form.get("batch").upper()
        subject = request.form.get("subject").upper()

        students, marks = find_topper(dept, year, semester, batch, subject)
    return render_template("index.html", students = students, marks = marks)

if __name__ == "__main__":
    app.run(debug=True)
