from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import resume_score_calculator
import send_mail
#from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "abhi"
app.permanent_session_lifetime = timedelta(minutes=10)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite://///home/abhimat/Desktop/full/app/database.db'       #paste path of database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class user_db(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(80))
    
    def __init__(self,user_name,name,email,password):
        
        self.name = name
        self.email = email
        self.password = password
        self.user_name = user_name

class user_details(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80),unique=True)
    resume_link = db.Column(db.String(100))
    address = db.Column(db.String(100))
    cgpa = db.Column(db.String(3))
    phone_number = db.Column(db.String(10))

    def __init__(self,user_name,name,email,resume_link,address,cgpa, phone_number):    
        self.name = name
        self.email = email
        self.user_name = user_name
        self.resume_link = resume_link
        self.address = address
        self.cgpa = cgpa
        self.phone_number = phone_number

class job(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(4), unique=True)
    company_name = db.Column(db.String(50))
    position = db.Column(db.String(50))
    required_skill = db.Column(db.String(50))
    job_description = db.Column(db.String(300))
    cgpa_cutoff = db.Column(db.String(3))

    def __init__(self,job_id,company_name,position,required_skill,job_description, cgpa_cutoff):
        self.job_id = job_id
        self.company_name = company_name
        self.required_skill = required_skill
        self.job_description = job_description
        self.position = position
        self.cgpa_cut = cgpa_cutoff

class job_applied(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80))
    applied = db.Column(db.String(100))

    def __init__(self,user_name,applied):
        self.user_name = user_name
        self.applied= applied


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')





@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if "user" in session:
        user_name = session["user"]
        found_user = user_db.query.filter_by(user_name=user_name).first()
        found_user_details = user_details.query.filter_by(user_name=user_name).first()
        if found_user_details:
            if request.method =='POST':
                cgpa = request.form['cgpa']
                address = request.form['address']
                resume_link = request.form['resume_link']
                phone_number = request.form['phone_number']
                if cgpa:
                    found_user_details.cgpa = cgpa
                if address:
                    found_user_details.address = address
                if resume_link:
                    found_user_details.resume_link = resume_link
                db.session.commit()
                return render_template('profile.html',user_name = user_name, email =found_user.email, name =found_user.name, address =found_user_details.address, resume_link = found_user_details.resume_link, cgpa = found_user_details.cgpa, user=user_name, phone_number=found_user_details.phone_number)        
            return render_template('profile.html',user_name = user_name, email =found_user.email, name =found_user.name, address =found_user_details.address, resume_link = found_user_details.resume_link, cgpa = found_user_details.cgpa,user=user_name, phone_number=found_user_details.phone_number)
        if request.method =='POST':
            cgpa = request.form['cgpa']
            address = request.form['address']
            resume_link = request.form['resume_link']
            phone_number = request.form['phone_number']
            if cgpa or address or resume_link or phone_number:
                usr = user_details(user_name, found_user.name, found_user.email, resume_link, address, cgpa, phone_number)
                db.session.add(usr)
                db.session.commit()
                return render_template('profile.html',user_name = user_name, email =found_user.email, name =found_user.name, address =address, resume_link = resume_link, cgpa = cgpa,user=user_name, phone_number=phone_number)
        return render_template('profile.html', user_name=user_name, email =found_user.email, name =found_user.name,user=user_name)
    else:
        return redirect(url_for("login"))




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        user_name = request.form['user_name']
        email = request.form['email']
        s = email
        password = request.form['password']
        found_user = user_db.query.filter_by(user_name=user_name).first()
        found_user_email = user_db.query.filter_by(email=email).first()
        s = s[-10:]
        if s == 'thapar.edu':     
            if found_user or found_user_email:
                return render_template('register.html',msg = "User Already Exist change User Name or Email")
            else:
                usr = user_db(user_name,name,email,password)
                db.session.add(usr)
                db.session.commit()
                return render_template('register.html',msg = "Profile created, please go to login page to continue")
        else:
            return render_template('register.html',msg = "Please use Thapar Mail Only")
    return render_template('register.html')





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        email = request.form['email']
        password = request.form['password']
        if user_name and email and password:
            found_user = user_db.query.filter_by(user_name=user_name).first()
            if found_user:
                if found_user.user_name == "abhi0444" and found_user.email == email and found_user.password == password:
                    session.permanent = True
                    session["user"] = found_user.user_name
                    return redirect(url_for("dashboard_admin"))
                if found_user.email == email and found_user.password == password:
                    session.permanent = True
                    session["user"] = found_user.user_name
                    return redirect(url_for("profile"))
                else:
                    return render_template('login.html',msg="Invalid password or Email")
            else:
                return render_template('login.html',msg="Username Not found")
        else:
            return render_template('login.html',msg="All above fields are required")
    else:
        return render_template('login.html', msg="Enter Details")





@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if "user" in session:
        user_name = session["user"]
        if request.method == 'POST':
            job1 = request.form['job_id']
            return redirect(url_for("job_display", job1 = job1))
        else:
            found = job.query.all()
            found_user = job_applied.query.filter_by(user_name=user_name).first()
            if found_user:
                app_jobs = found_user.applied
                app_jobs = app_jobs.split(' ')
                job_id = []
                company_name = []
                job_description = []
                position = []
                for item in found:
                    if item.job_id not in app_jobs:
                        job_id.append(item.job_id)
                        company_name.append(item.company_name)
                        job_description.append(item.job_description)
                        position.append(item.position)
                dict = {}
                dict['job_id'] = job_id
                dict['company_name'] = company_name
                dict['job_description'] = job_description
                dict['position'] = position
                return render_template('dashboard.html', dict = dict, k = len(dict['job_id']),user=user_name)
            else:
                job_id = []
                company_name = []
                job_description = []
                position = []
                for item in found:
                    job_id.append(item.job_id)
                    company_name.append(item.company_name)
                    job_description.append(item.job_description)
                    position.append(item.position)
                dict = {}
                dict['job_id'] = job_id
                dict['company_name'] = company_name
                dict['job_description'] = job_description
                dict['position'] = position
                return render_template('dashboard.html', dict = dict, k = len(dict['job_id']),user=user_name)
    else:
        return redirect(url_for("login"))





@app.route('/dashboard_admin', methods=['GET', 'POST'])
def dashboard_admin():
    if "user" in session:
        user_name = session["user"]
        if user_name == "abhi0444":
            if request.method == "POST":
                job_id = request.form['job_id']
                return redirect(url_for('job_score', job_id = job_id))
            else:
                return render_template('dashboard_admin.html', data = job.query.all(),user='user_name')
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))




@app.route('/job_input' , methods=['GET', 'POST'])
def job_input():
    if "user" in session:
        user_name = session["user"]
        if user_name == "abhi0444":
            if request.method == 'POST':
                job_id = request.form['job_id']
                company_name = request.form['company_name']
                skills = request.form['skills']
                job_description = request.form['job_description']
                position = request.form['position']
                cgpa_cutoff = request.form['cgpa_cutoff']
                if job_id and company_name and skills and job_description and position:
                    usr = job(job_id, company_name, position, skills, job_description, cgpa_cutoff)
                    db.session.add(usr)
                    db.session.commit()
                    return render_template('job_input.html', msg = "JOB ADDED",user=user_name)
            return render_template('job_input.html', msg="Nothing Changed",user=user_name)
        return redirect(url_for("login"))
    return redirect(url_for("login"))






@app.route('/applied_jobs')
def applied_jobs():
    if "user" in session:
        user_name = session["user"]
        found_user = job_applied.query.filter_by(user_name=user_name).first()
        if found_user:
            app_jobs = found_user.applied
            app_jobs = app_jobs.split(' ')
            job_description = []
            job_id = []
            company_name = []
            required_skill = []
            position = []
            for item in app_jobs:
                found = job.query.filter_by(job_id = item).first()
                job_id.append(item)
                company_name.append(found.company_name)
                required_skill.append(found.required_skill)
                job_description.append(found.job_description)
                position.append(found.position)
            dict = {}
            dict['job_id'] = job_id
            dict['company_name'] = company_name
            dict['required_skill'] = required_skill
            dict['job_description'] = job_description
            dict['position'] = position
            return render_template('applied_jobs.html', dict = dict, k = len(dict['job_id']), user=user_name)
        else:
            return render_template('applied_jobs.html', k =0 ,msg = "No jobs Applied", user=user_name)

    return redirect(url_for("login"))





@app.route("/<job_id>", methods=['GET', 'POST'])
def job_score(job_id):
    if "user" in session:
        user_name = session["user"]
        if user_name == "abhi0444":
            found = job_applied.query.all()
            company = []
            user_name_list = []
            name =[]
            resume_link = []
            for item in found:
                app_job = item.applied
                app_jobs = app_job.split(' ')
                if job_id in app_jobs:
                    user_name_list.append(item.user_name)
                    found_name = user_details.query.filter_by(user_name=item.user_name).first()
                    name.append(found_name.name)
                    resume_link.append(found_name.resume_link)
            dict = {}
            found_job = job.query.filter_by(job_id=job_id).first()            
            #company.append(found_job.company_name)
            dict ['job_id'] = job_id
            dict['user_name'] = user_name_list
            dict['resume_link'] = resume_link
            dict['name'] = name
            #dict['company_name'] = company

            if request.method == 'POST':
                dicte = request.form['job_id']
                cv_score = []
                total_score = []
                for i in range(0, len(dict['resume_link'])):            #inputs = (link, user_name, skills, cgpa)
                    found_job = job.query.filter_by(job_id=job_id).first()
                    skills = found_job.required_skill
                    skills = skills.split(' ')
                    found_user = user_details.query.filter_by(user_name=dict['user_name'][i]).first()
                    cgpa = found_user.cgpa
                    user_n = dict['user_name'][i]
                    link = dict['resume_link'][i]
                    val = resume_score_calculator.calculate_score(link,user_n, skills, cgpa) 
                    cv_score.append(val[0])
                    total_score.append(val[1])
                dict['cv_score'] = cv_score
                dict['total_score'] = total_score
                session['dict'] = dict
                return redirect(url_for('eveluate'))

            else:
                return render_template("job_score.html", dict= dict, k = len(dict['name']), user=user_name)
        else:
            found_job = job.query.filter_by(job_id=job_id).first()
            if request.method == 'POST':
                job_id = request.form['job_id']
                found = job_applied.query.filter_by(user_name=user_name).first()
                if found:
                    prev_applied = found.applied
                    l = prev_applied.split(' ')
                    if job_id in l:
                        1
                    else:
                        prev_applied = prev_applied + ' ' +job_id
                        found.applied =prev_applied
                        db.session.commit()
                    return render_template('job_display.html', job1 = found_job, user=user_name)
                else:
                    usr = job_applied(user_name,job_id)
                    db.session.add(usr)
                    db.session.commit()
            if found_job:
                return render_template('job_display.html', job1 = found_job, user=user_name)

            return render_template('job_display.html', job1 = found_job , user=user_name)

    else:
        return redirect(url_for("login"))




@app.route('/<job1>', methods=['GET', 'POST'])
def job_display(job1):
    if "user" in session:
        user_name = session["user"]
        found_job = job.query.filter_by(job_id=job1).first()
        if request.method == 'POST':
            job1 = request.form['job_id']
            found = job_applied.query.filter_by(user_name=user_name).first()
            if found:
                prev_applied = found.applied
                l = prev_applied.split(' ')
                if job1 in l:
                    1
                else:
                    prev_applied = prev_applied + ' ' +job1
                    found.applied =prev_applied
                    db.session.commit()
                return render_template('job_display.html', job1 = found_job, user=user_name)
            else:
                usr = job_applied(user_name,job1)
                db.session.add(usr)
                db.session.commit()
        if found_job:
            return render_template('job_display.html', job1 = found_job, user=user_name)

        return render_template('job_display.html', job1 = found_job, user=user_name)
    else:
        return redirect(url_for("login"))




@app.route("/eveluate", methods=['GET', 'POST'])
def eveluate():
    if "user" in session:
        user_name = session["user"]
        if user_name == "abhi0444":
            dict = session["dict"]
            if request.method == 'POST':
                cutoff = request.form['cutoff']
                found = job.query.all()
                company_name = []
                for item in found:
                    if item.job_id == dict['job_id']:
                        company_name.append(item.company_name)
                        break
                for i in range(0,len(dict['cv_score'])):        
                    found_user = user_details.query.filter_by(user_name=dict['user_name'][i]).first()  #send(e_mail_sender,name,company,action(int),p):
                    if(float(dict['cv_score'][i]) == float(0)):
                        send_mail.send(found_user.email,found_user.name,company_name[0],1,0)
                    else:
                        if float(dict['total_score'][i]) > float(cutoff):
                            send_mail.send(found_user.email,found_user.name,company_name[0],1,1)
                        else:
                            send_mail.send(found_user.email,found_user.name,company_name[0],0,1)
                return render_template('eveluate.html', dict = dict, k = len(dict['name']), msg = "Email sent to user", user=user_name)
            else:
                return render_template('eveluate.html', dict = dict, k = len(dict['name']), user=user_name)
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))




@app.route("/logout",)
def logout():
    session.pop("user",None)
    return redirect(url_for("index", msg="Logout Successful"))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)