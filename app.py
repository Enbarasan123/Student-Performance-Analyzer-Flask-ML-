from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.secret_key = "secret123"

# ================= DB =================
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users VALUES('admin','admin')")

    cur.execute("""CREATE TABLE IF NOT EXISTS students(
        name TEXT,
        tamil INT,
        english INT,
        math INT,
        science INT,
        social INT,
        total INT
    )""")

    conn.commit()
    conn.close()

init_db()

def get_db():
    return sqlite3.connect("database.db")

# ================= ML =================
X = np.array([
    [80,70,90,85,88],
    [60,65,70,60,58],
    [90,92,95,94,96],
    [50,55,60,58,52]
])
y = np.sum(X, axis=1)

model = LinearRegression()
model.fit(X, y)

def predict_score(marks):
    return round(model.predict([marks])[0], 2)

# ================= LOGIC =================
def check_pass_fail(marks):
    for m in marks:
        if m < 35:
            return "Fail"
    return "Pass"

def generate_plan(marks):
    subjects = ["Tamil","English","Math","Science","Social"]
    plan = []
    for s, m in zip(subjects, marks):
        if m < 50:
            plan.append(f"{s}: 2.5 hrs/day")
        elif m < 70:
            plan.append(f"{s}: 2 hrs/day")
        else:
            plan.append(f"{s}: 1 hr/day")
    return plan

def generate_suggestions(marks):
    subjects = ["Tamil","English","Math","Science","Social"]
    suggestions = []
    avg = sum(marks)/len(marks)

    for s, m in zip(subjects, marks):
        if m < 35:
            suggestions.append(f"⚠️ Critical: Improve {s}")
        elif m < 70:
            suggestions.append(f"📘 Improve {s}")
        else:
            suggestions.append(f"✅ Strong in {s}")

    if avg < 60:
        suggestions.append("🔥 Overall low performance")
    elif avg < 80:
        suggestions.append("📈 Good performance")
    else:
        suggestions.append("🏆 Excellent")

    return suggestions

# ================= ROUTES =================
@app.route("/", methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        data = cur.fetchone()
        conn.close()

        if data:
            session["user"] = user
            return redirect("/dashboard")
        else:
            error = "Invalid Credentials"

    return render_template("login.html", error=error)


@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    conn = get_db()
    cur = conn.cursor()

    prediction = None
    plan = []
    suggestions = []
    status = None
    prev_marks = []
    current_marks = []

    search_query = request.args.get("search")
    filter_type = request.args.get("filter")

    if request.method == "POST":
        name = request.form["name"]

        current_marks = [
            int(request.form["tamil"]),
            int(request.form["english"]),
            int(request.form["math"]),
            int(request.form["science"]),
            int(request.form["social"])
        ]

        prev_marks = [
            int(request.form["ptamil"]),
            int(request.form["penglish"]),
            int(request.form["pmath"]),
            int(request.form["pscience"]),
            int(request.form["psocial"])
        ]

        total = sum(current_marks)

        prediction = predict_score(current_marks)
        plan = generate_plan(current_marks)
        suggestions = generate_suggestions(current_marks)
        status = check_pass_fail(current_marks)

        cur.execute("INSERT INTO students VALUES (?,?,?,?,?,?,?)",
                    (name, *current_marks, total))
        conn.commit()

    cur.execute("SELECT * FROM students")
    data = cur.fetchall()

    if search_query:
        data = [d for d in data if search_query.lower() in d[0].lower()]

    totals = [d[-1] for d in data]

    # Correct pass/fail
    statuses = ["Pass" if all(m >= 35 for m in d[1:6]) else "Fail" for d in data]

    leaderboard = sorted(data, key=lambda x: x[-1], reverse=True)

    if filter_type == "pass":
        leaderboard = [s for s in leaderboard if all(m >= 35 for m in s[1:6])]
    elif filter_type == "fail":
        leaderboard = [s for s in leaderboard if any(m < 35 for m in s[1:6])]

    return render_template("dashboard.html",
                           totals=totals,
                           statuses=statuses,
                           leaderboard=leaderboard,
                           prediction=prediction,
                           plan=plan,
                           suggestions=suggestions,
                           status=status,
                           prev_marks=prev_marks,
                           current_marks=current_marks)


@app.route("/export_pdf")
def export_pdf():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()

    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Student Report", styles['Title']))
    content.append(Spacer(1,10))

    for s in data:
        content.append(Paragraph(f"{s[0]} - Total: {s[-1]}", styles['Normal']))
        content.append(Spacer(1,5))

    doc.build(content)

    return send_file("report.pdf", as_attachment=True)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)