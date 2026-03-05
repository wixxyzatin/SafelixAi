from flask import Flask, render_template, request, redirect, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "safelix_secret"


# ================= DATABASE INIT =================
def init_db():
    conn = sqlite3.connect("startup.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS analyses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idea TEXT,
        budget TEXT,
        team TEXT,
        score INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()


# ================= LOGIN =================
@app.route('/', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("startup.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email,password))
        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = user[1]
            return redirect('/dashboard')

        return "Invalid login"

    return render_template("login.html")


# ================= SIGNUP =================
@app.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("startup.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",
                    (name,email,password))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template("signup.html")


# ================= DASHBOARD =================
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template("dashboard.html")


# ================= ANALYZER =================
@app.route('/analyzer')
def analyzer():
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze():

    idea = request.form['idea']
    budget = request.form['budget']
    team = request.form['team']

    score = random.randint(50, 95)

    conn = sqlite3.connect("startup.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO analyses(idea,budget,team,score) VALUES(?,?,?,?)",
                (idea,budget,team,score))
    conn.commit()
    conn.close()

    return render_template("result.html", idea=idea)


# ================= GENERATE =================
@app.route('/generate', methods=['GET','POST'])
def generate():

    if request.method == 'POST':

        industry = request.form['industry']
        skills = request.form['skills']
        budget = request.form['budget']
        interest = request.form['interest']

        idea_output = f"""
Startup Name: Smart {industry.capitalize()} Platform

Problem:
People in the {industry} sector struggle with efficiency.

Solution:
Using {skills}, build a platform improving {industry} experiences.

Target Users:
People interested in {interest}

Revenue Model:
Subscription + premium services.

MVP:
Launch a simple version solving one major {industry} issue.

Pitch:
A scalable {industry} startup transforming {interest}.
"""

        return render_template("result.html", idea=idea_output)

    return render_template("generate.html")


# ================= PITCH =================
@app.route('/pitch', methods=['GET','POST'])
def pitch():

    if request.method == 'POST':

        startup = request.form['startup']
        industry = request.form['industry']
        problem = request.form['problem']
        solution = request.form['solution']

        pitch_text = f"""
Startup: {startup}

Industry:
{industry}

Problem:
{problem}

Solution:
{solution}

Market Opportunity:
Growing demand in {industry} sector.

Revenue Model:
Subscription + partnerships.

Growth Plan:
Launch MVP → scale users → expand market.

Funding Ask:
Seeking seed investment.

30-sec Pitch:
{startup} is a {industry} startup solving {problem}.
We provide {solution}.
This creates scalable opportunity in growing market.
"""

        return render_template("pitch.html", pitch=pitch_text)

    return render_template("pitch.html")


# ================= INVESTOR =================
@app.route('/investor', methods=['GET','POST'])
def investor():

    if request.method == 'POST':

        score = random.randint(55, 90)

        if score > 75:
            status = "High investment potential"
        elif score > 60:
            status = "Moderate potential"
        else:
            status = "High risk startup"

        return render_template("investor.html", score=score, status=status)

    return render_template("investor.html")


# ================= VIEW =================
@app.route('/view')
def view():

    conn = sqlite3.connect("startup.db")
    cur = conn.cursor()
    cur.execute("SELECT idea,budget,team,score FROM analyses")
    data = cur.fetchall()
    conn.close()

    return render_template("view.html", data=data)


# ================= ABOUT =================
@app.route('/about')
def about():
    return render_template("about.html")


# ================= ADMIN =================
@app.route('/admin')
def admin():

    conn = sqlite3.connect("startup.db")
    cur = conn.cursor()
    cur.execute("SELECT idea,budget,team,score FROM analyses")
    data = cur.fetchall()
    conn.close()

    return render_template("admin.html", data=data)


# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
