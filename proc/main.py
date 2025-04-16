from flask import Flask, render_template, request, redirect, url_for
import datub

datub.drop_datubazi()
app = Flask(__name__)
datub.create_datubazi()

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
    
@app.route('/login', methods=["GET", "POST"])
def forma():
    if request.method == "POST":
        vards = request.form.get('name')
        uzvards = request.form.get('uzvards')
        parole = request.form.get('parole')
        print(vards, uzvards, parole)
        return render_template("login.html", iesniegts = True)
    else:
        return render_template("login.html", iesniegts = False)  
    
@app.route('/registr', methods=["GET", "POST"])
def forma1():
    if request.method == "POST":
        vards1 = request.form.get('name1')
        uzvards1 = request.form.get('uzvards1')
        klase1 = request.form.get('klase1')
        parole1 = request.form.get('parole1')
        print(vards1, uzvards1, klase1, parole1)
        return render_template("registr.html", iesniegts = True)
    else:
        return render_template("registr.html", iesniegts = False)  


if __name__ == '__main__':
    app.run(debug=True)
