from flask import Flask, render_template, request, redirect, url_for, session
import datub
import calendar
from datetime import datetime

app = Flask(__name__)
# datub.drop_datubazi()
# datub.create_datubazi()

@app.route('/')
def index():
    events = datub.get_events()
    role = session.get('role')
    return render_template('index.html', events=events, role=role)

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

@app.route('/kalendars')
def kalendars():
    gads = int(request.args.get('gads', session.get('gads', datetime.now().year)))
    menesis = int(request.args.get('menesis', session.get('menesis', datetime.now().month)))

    session['gads'] = gads
    session['menesis'] = menesis

    cal = calendar.monthcalendar(gads, menesis)
    month_name = calendar.month_name[menesis]

    events = datub.get_events()
    month_events = {}
    
    for event in events:
        try:
            event_date = datetime.strptime(event['time'].split(', ')[1], "%d.%m.%Y")
            if event_date.year == gads and event_date.month == menesis:
                day = event_date.day
                if day not in month_events:
                    month_events[day] = []
                month_events[day].append(event)
        except (IndexError, ValueError):
            continue

    return render_template('kalendars.html', 
                         gads=gads, 
                         menesis=menesis,
                         month_name=month_name,
                         cal=cal,
                         month_events=month_events,
                         datetime=datetime)

@app.route('/day_events/<int:gads>/<int:menesis>/<int:day>')
def day_events(gads, menesis, day):
    date_str = f"{day:02d}.{menesis:02d}.{gads}"
    events = datub.get_events_by_date(date_str)
    
    if len(events) == 1:
        return redirect(url_for('event_detail', event_id=events[0]['id']))
    
    # TODO ЗДЕСЬ ИСПОЛЬЗУЕМ РОЛЬ
    return render_template('day_events.html', 
                         events=events,
                         date_str=date_str,
                         gads=gads,
                         menesis=menesis,
                         day=day,
                         role = session.get('role'))

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
def login():
    admin_parole = 'superparole'
    if request.method == "POST":
        vards = request.form.get('name')
        uzvards = request.form.get('uzvards')
        parole = request.form.get('parole')
        if parole == admin_parole:
            session['role'] == 'Admin'
        users = datub.get_user(vards, uzvards, parole)
        if users:
            session['user'] = vards
            # TODO ЗДЕСЬ ИНФА ПРО РОЛЬ
        else:
            session.get('role') == users[-1]
            return redirect(url_for('index'))
    else:
        return render_template("login.html", error="Nepareizs vārds vai parole")
    return render_template("login.html")

@app.route('/registr', methods=["GET", "POST"])
def registr():
    if request.method == "POST":
        vards = request.form.get('name')
        uzvards = request.form.get('uzvards')
        klase = request.form.get('klase')
        parole = request.form.get('parole')
        users_id = datub.register_user(vards, uzvards, parole, klase)
        if users_id:
            return redirect(url_for('index'))
        else:
            return render_template("registr.html", iesniegts=False)
    return render_template("registr.html", iesniegts=False)

@app.route('/logout')
def logout():
    session.pop('role', None)
    return redirect(url_for('index'))

# @app.route('/profile')

# def profile():
#     user = session.get('user')
#     if not user:
#         return redirect(url_for('forma'))
#     return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
