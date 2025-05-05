from flask import Flask, render_template, request, redirect, url_for, session, flash
import datub # datub.py ir fails kurā ir izveidota datubaze un funkcijas, lai ierakstītu datus
import calendar
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supermamaboboclat'#lai varētu izmantot sesijas un varētu saglabāt datus starp lapām, kā arī drošības nolūkos
# datub.drop_datubazi()
# datub.create_datubazi()

@app.route('/')
def index():
    events = datub.get_events()  # iegūst visus pasākumus no datubāzes
    role = session.get('role')  # sesija ir Flaskā, kas ļauj saglabāt datus starp lapām, ļauj uzturēt cilvēka reģistrētos datus
    user = session.get('user')  # session.get('user') uztur lietotāja informāciju, ar ko ir reģistrējies
    applied_events = []
    if user and role == "Student":
        applied_events = datub.get_user_applied_events(user)  # ja ir reģistrējies kā students, tad iegūst visus pasākumus, kuros ir pieteicies
    return render_template('index.html', events=events, role=role, user=user, applied_events=applied_events)

@app.route('/events')
def all_events():
    role = session.get('role')  # sesija ir Flaskā, kas ļauj saglabāt datus starp lapām, ļauj uzturēt cilvēka reģistrētos datus
    user = session.get('user')
    events = datub.get_events()
    applied_events = []
    if user and role == "Student":
        applied_events = datub.get_user_applied_events(user)
    return render_template('events.html', events=events, role=role, user=user, applied_events=applied_events)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    events = datub.get_events()
    event = next((activity for activity in events if activity['id'] == event_id), None)#sameklē pirmo objektu listā, un tad meklē pasākumus pēc to ID, lai sakristu activity['id'] ar event_id, un tad atgriež pareizo pasākumu. Ir uzrakstīt None, ja nav atrasts neviens pasākums
    if not event:#ja nav atrasts pasākums, tad atgriež ziņu, ka nav atrasts pasākums
        return "Tāda pasākuma nav"
    return render_template('event.html', event=event)

@app.route('/kalendars')
def kalendars():
    gads = int(request.args.get('gads', session.get('gads', datetime.now().year)))
    menesis = int(request.args.get('menesis', session.get('menesis', datetime.now().month)))

    session['gads'] = gads
    session['menesis'] = menesis

    cal = calendar.monthcalendar(gads, menesis)# izveido kalendāru, konkrētam mēnesim un gadam, ar nedēļām un dienām
    month_name = calendar.month_name[menesis]# iegūstam mēneša nosaukumu pēc tā numura

    events = datub.get_events()
    month_events = {}
    
    for event in events:
        try:
            event_date = datetime.strptime(event['time'].split(', ')[1], "%d.%m.%Y")#ie
            if event_date.year == gads and event_date.month == menesis:
                day = event_date.day
                if day not in month_events:
                    month_events[day] = []
                month_events[day].append(event)
        except (IndexError, ValueError):#
            continue

    return render_template('kalendars.html', 
                         gads=gads, 
                         menesis=menesis,
                         month_name=month_name,
                         cal=cal,
                         month_events=month_events,
                         datetime=datetime)# izveido kalendāru, kurā ir pasākumi, kas notiek konkrētā dienā

def day_events(gads, menesis, day):
    date_str = f"{day:02d}.{menesis:02d}.{gads}"#formāts datumam, 2 cipari katram skaitlim
    events = datub.get_events_by_date(date_str)
    
    if len(events) == 1:# ja ir tikai viens pasākums dienā, tad tevi aizved uz pasākuma informācijas lapu
        return redirect(url_for('event_detail', event_id=events[0]['id']))
    
    return render_template('day_events.html', 
                         events=events,
                         date_str=date_str,
                         gads=gads,
                         menesis=menesis,
                         day=day) 
# Pogas nākamajam mēnesim
@app.route('/kalendars/nakamais')
def nakamais_menesis():
    gads = session.get('gads', datetime.now().year)
    menesis = session.get('menesis', datetime.now().month)

    if menesis == 12:#ja, piemēram, ir decembris, tad nākamais mēnesis būs janvāris un gads ir jāpalielina par 1
        menesis = 1
        gads += 1
    else:#ja ir cits mēnesis, tad palielinām mēnesi par 1, lai būtu nākamais mēnesis
        menesis += 1

    return redirect(url_for('kalendars', gads=gads, menesis=menesis))


# Pogas iepriekšējam mēnesim
@app.route('/kalendars/ieprieksejais')
def ieprieksejais_menesis():
    gads = session.get('gads', datetime.now().year)
    menesis = session.get('menesis', datetime.now().month)

    if menesis == 1:#ja, piemēram, ir janvāris, tad iepriekšējais mēnesis būs decembris un gads ir jāsamazina par 1
        menesis = 12
        gads -= 1
    else:#ja ir cits mēnesis, tad samazinām mēnesi par 1, lai būtu iepriekšējais mēnesis
        menesis -= 1

    return redirect(url_for('kalendars', gads=gads, menesis=menesis))
    
@app.route('/login', methods=["GET", "POST"])
def login():
    admin_parole = 'superparole'#parole, kas ir jāievada, lai reģistrētos kā admins
    if request.method == "POST":#ja ir izmantota POST metode, tad iegūst datus no formas
        vards = request.form.get('name')#iegūstam cilvēka vārdu no formas utt
        uzvards = request.form.get('uzvards')
        parole = request.form.get('parole')
        if parole == admin_parole:#ja parole ir superparole, tad cilvēks ir admins
            session['role'] = 'Admin'
            session['user'] = vards
            return redirect(url_for('index'))
        users = datub.get_user(vards, uzvards, parole)#ja parole ir pareiza, tad iegūstam cilvēka datus no datubāzes
        if users:#ja ir atrasts cilvēks datubāzē, tad saglabājam datus sesijā un pāradresējam uz index lapu
            session['role'] = users[-1] #pieņemam, ka loma ir pēdējais elements sarakstā
            session['user'] = vards
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="Nepareizs vārds vai parole")# ja nav atrasts cilvēks datubāzē, tad atgriežam kļūdas ziņu un prasa no jauna pieslēgties
    return render_template("login.html")

@app.route('/registr', methods=["GET", "POST"])
def registr():
    admin_parole = 'superparole'#parole, kas ir jāievada, lai reģistrētos kā admins
    if request.method == "POST":#ja ir izmantota POST metode, tad iegūst datus no formas
        vards = request.form.get('name')#iegūstam cilvēka vārdu no formas utt
        uzvards = request.form.get('uzvards')
        klase = request.form.get('klase')
        parole = request.form.get('parole')
        if parole == admin_parole:#ja parole ir superparole, tad cilvēks ir admins, ja nē, tad students
            session['role'] = 'Admin'
        else:
            session['role'] = 'Student' 
        users_id = datub.register_user(vards, uzvards, parole, klase, session['role'])#reģistrējam cilvēku datubāzē, ja parole ir pareiza, tad  kā admin, ja nē, tad kā studentu
        if users_id:#ja ir reģistrējies cilvēks, tad saglabājam datus sesijā un pāradresējam uz index lapu
            session['user'] = vards
            session['role'] = session['role'] 
            return redirect(url_for('index'))
        else:
            return render_template("index.html")
    return render_template("registr.html")

@app.route('/logout')
def logout():
    session.clear()#iztīra sesiju. Izdzēš visus datus no sesijas, kas ir saglabāti
    return redirect(url_for('index'))

@app.route('/apply/<int:event_id>', methods=["POST"])
def pieteikties(event_id):
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    # Veic pieteikšanos pasākumam
    success = datub.apply_for_event(user, event_id)
    if success:
        return render_template("booking.html", success="Pieteikšanās veiksmīga")
    else:
        return render_template("booking.html", error="Pieteikšanās neizdevās")
@app.route('/user_list')
@app.route('/user_list/<int:event_id>')
def user_list(event_id=None):#iesgūstam pieteikušos skolēnus
    if session.get('role') != 'Admin':# ja loma nav admins, tad pāriet uz index lapu
        return redirect(url_for('index'))
    
    participants = datub.get_event_participants(event_id)
    return render_template('user_list.html', 
                        participants=participants,
                        event_id=event_id)

if __name__ == '__main__':
    app.run(debug=True)
