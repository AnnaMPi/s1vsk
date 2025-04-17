from flask import Flask, render_template, request, redirect, url_for, session
import datub
import calendar
from datetime import datetime

datub.drop_datubazi()
app = Flask(__name__)
datub.create_datubazi()

app.secret_key = 'superparole'

@app.route('/')
def index():
    events = datub.get_events()
    return render_template('index.html', events=events)
@app.route('/events')
def all_events():
    events = datub.get_events()
    return render_template('events.html', events=events)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    events = datub.get_events()
    event = next((activity for activity in events if activity['id'] == event_id), None)
    if not event:
        return "Tāda pasakuma nav", 404
    return render_template('event.html', event=event)

    
@app.route('/booking/success')
def booking_success():
    return "👌"

# @app.route('/kalendars')
# def calendars():
#     yy = 2025
#     # mm = 4
#     cal = calendar.calendar(yy)
#     return render_template('kalendars.html', yy=yy, cal=cal)
@app.route('/kalendars')
def kalendars():
    # Iegūst gadu un mēnesi no vaicājuma parametriem vai sesijas
    gads = int(request.args.get('gads', session.get('gads', datetime.now().year)))
    menesis = int(request.args.get('menesis', session.get('menesis', datetime.now().month)))

    # Saglabājam gadu un mēnesi sesijā
    session['gads'] = gads
    session['menesis'] = menesis

    # Ģenerējam kalendāra tekstu
    kal = calendar.month(gads, menesis)

    return render_template('kalendars.html', gads=gads, menesis=menesis, kal=kal)

# Pogas nākamajam mēnesim
@app.route('/kalendars/nakamais')
def nakamais_menesis():
    gads = session.get('gads', datetime.now().year)
    menesis = session.get('menesis', datetime.now().month)

    if menesis == 12:
        menesis = 1
        gads += 1
    else:
        menesis += 1

    return redirect(url_for('kalendars', gads=gads, menesis=menesis))


# Pogas iepriekšējam mēnesim
@app.route('/kalendars/ieprieksejais')
def ieprieksejais_menesis():
    gads = session.get('gads', datetime.now().year)
    menesis = session.get('menesis', datetime.now().month)

    if menesis == 1:
        menesis = 12
        gads -= 1
    else:
        menesis -= 1

    return redirect(url_for('kalendars', gads=gads, menesis=menesis))
    
@app.route('/login', methods=["GET", "POST"])
def forma():
    if request.method == "POST":
        vards = request.form.get('name')
        uzvards = request.form.get('uzvards')
        parole = request.form.get('parole')
        students = datub.get_user(vards, uzvards, parole)
        if students:
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error = "Nepareiz vārds vai uzvārds")
    return render_template("login.html")

    
@app.route('/registr', methods=["GET", "POST"])
def forma1():
    if request.method == "POST":
        vards = request.form.get('name')
        uzvards = request.form.get('uzvards')
        klase = request.form.get('klase')
        parole = request.form.get('parole')
        students_id = datub.register_user(vards, uzvards, parole, klase)
        if students_id:
            return redirect(url_for('index'))
        else:
            return render_template("registr.html", iesniegts=True, students_id=students_id)
    return render_template("registr.html", iesniegts=False) 


if __name__ == '__main__':
    app.run(debug=True)
