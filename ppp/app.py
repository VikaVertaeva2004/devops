from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppp.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    home_phone = db.Column(db.String(20))
    work_phone = db.Column(db.String(20))
    commissions = db.relationship('CommissionMembership', backref='member', lazy=True)

class CommissionMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    commission_id = db.Column(db.Integer, db.ForeignKey('commission.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)

class Commission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    chairperson_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    memberships = db.relationship('CommissionMembership', backref='commission', lazy=True)
    meetings = db.relationship('Meeting', backref='commission', lazy=True)

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commission_id = db.Column(db.Integer, db.ForeignKey('commission.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    attendees = db.Column(db.Text)

@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/add_comission', methods=['GET', 'POST'])
def add_comission():
    if request.method == 'POST':
        name = request.form['name']
        chairperson_id = request.form.get('chairperson_id', None)  # Получаем chairperson_id из формы, если он есть
        new_commission = Commission(name=name, chairperson_id=chairperson_id)

        db.session.add(new_commission)
        db.session.commit()

        # Добавление членов в комиссию, если они выбраны
        member_ids = request.form.getlist('members')
        for member_id in member_ids:
            membership = CommissionMembership(
                member_id=member_id,
                commission_id=new_commission.id,
                start_date=datetime.now()
            )
            db.session.add(membership)

        db.session.commit()
        return redirect(url_for('commissions'))

    members = Member.query.all()
    return render_template('add_comission.html', members=members)

@app.route("/add_meeting", methods=['GET', 'POST'])
def add_meeting():
    return render_template("add_meeting.html")

@app.route("/add_member", methods=['POST', 'GET'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        home_phone = request.form['home_phone']
        work_phone = request.form['work_phone']

        member = Member(name=name, address=address, home_phone=home_phone, work_phone=work_phone)

        try:
            db.session.add(member)
            db.session.commit()
            return redirect('/')
        except:
            flash("Error while adding member.")
            return redirect(url_for('add_member'))
    else:
        return render_template('add_member.html')

@app.route("/comissions")
def commissions():
    commissions = Commission.query.all()
    return render_template('comissions.html', commissions=commissions)

@app.route('/meetings_count', methods=['GET', 'POST'])
def meetings_count():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        meeting_counts = db.session.query(
            Commission.name,
            db.func.count(Meeting.id)
        ).join(Meeting).filter(
            Meeting.datetime.between(start_date, end_date)
        ).group_by(Commission.id).all()

        return render_template('meetings_count.html', meeting_counts=meeting_counts)

    return render_template('meetings_count.html')

@app.route('/missed_meetings', methods=['GET', 'POST'])
def missed_meetings():
    if request.method == 'POST':
        commission_id = request.form['commission_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        missed_members = db.session.query(CommissionMembership).filter(
            CommissionMembership.commission_id == commission_id,
            # Обязательно проверьте, что `missed_meetings_count` определён, иначе это вызовет ошибку
            # например:
            # CommissionMembership.missed_meetings_count > 0
        ).all()

        return render_template('missed_meetings.html', missed_members=missed_members)

    commissions = Commission.query.all()
    return render_template('missed_meetings.html', commissions=commissions)

@app.route('/municipal_members')
def municipal_members():
    members = Member.query.all()
    member_commissions = {}

    for member in members:
        # Заменим на correct relationship name, if needed
        member_commissions[member] = member.commissions  # Обратите внимание на корректное использование

    return render_template('municipal_members.html', member_commissions=member_commissions)

@app.route("/posts")
def posts():
    return render_template('posts.html', posts=[])  # Передаём пустой список, поскольку posts не определен

@app.route("/create", methods=['POST', 'GET'])
def create():
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)