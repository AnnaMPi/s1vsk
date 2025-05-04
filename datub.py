import sqlite3
def drop_datubazi():
    conn = sqlite3.connect("datubazes.db")
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS events''')
    conn.commit()
    cursor.execute('''DROP TABLE IF EXISTS users''')
    conn.commit()
    cursor.execute('''DROP TABLE IF EXISTS pieteikties''')
    conn.commit()
    conn.close()

def create_datubazi():
    conn = sqlite3.connect("datubazes.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
                   id INTEGER PRIMARY KEY, 
                   title TEXT,
                   time TEXT,
                   poster TEXT,
                   description TEXT)''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pieteikties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (event_id) REFERENCES events(id))''')    

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   name TEXT,
                   surname TEXT,
                   password TEXT,
                   class TEXT,
                   role TEXT)''')
                   
    cursor.execute('''INSERT INTO events VALUES(1, "1.aprīls", "16:00, 1.04.2025", 'https://www.ozolniekuvsk.lv/wp-content/uploads/2022/03/aprilis.png', 'description')''')
    conn.commit()
    cursor.execute('''INSERT INTO events VALUES(2, "Eko diena", "14:00, 27.05.2025",'https://kekava.lv/wp-content/uploads/2023/04/Majaslapas-titulslaids18.png', 'descroriptoion')''')
    conn.commit()
    
    cursor.execute('''INSERT INTO events VALUES(3, "Žetona vakars", "17:00, 25.02.2025",'https://irv.lv/wp-content/uploads/2023/02/Afisa-1_zetoni.jpg', 'descroriptoion')''')
    conn.commit()



def register_user(vards, uzvards, parole, klase, role):
    conn = sqlite3.connect('datubazes.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, surname, password, class, role) VALUES (?, ?, ?, ?, ?)', (vards, uzvards, parole, klase, role)) # ievietojam mainīgos datus datubāzē
    conn.commit()
    users_id = c.lastrowid # iegūstam pēdējās ievietotās rindas ID
    conn.close()
    return users_id
    
def get_user(name, surname, password):
    conn = sqlite3.connect('datubazes.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name = ? AND surname = ? AND password = ?" #no tabulas users dabujam datus, kur vārds, uzvārds un parole ir vienādi ar ievadītajiem datiem
    cursor.execute(query, (name, surname, password))# iegūstam datus no datubāzes
    users = cursor.fetchone()#fetchone metode paņem vienu rindu no datubāzes konkrētam vaicājumam, ja nav vairs rindu, tad atgriež None
    conn.close()
    return users 

def get_events():
    conn = sqlite3.connect("datubazes.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM events''')
    events = cursor.fetchall()# paņem visus datus no tabulas events
    conn.close()

    events_dict = []
    for event in events:#iziet visiem elementiem kas ir zem events
        m = {#izveidojam jaunu mainīgo m, kurā ir iekļauti visi elementi
        'id': event[0],#iedodam nosaukumu un indexu
        'title': event[1],
        'description': event[4],
        'poster': event[3],
        'time': event[2]
        }

        events_dict.append(m)
    return events_dict

def get_events_by_date(date_str):
    conn = sqlite3.connect("datubazes.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM events WHERE time LIKE ?''', (f'%{date_str}%',))# meklējam visus pasākumus, kas notiek konkrētā datumā
    events = cursor.fetchall()
    conn.close()

    events_dict = []
    for event in events:
        m = {
            'id': event[0],
            'title': event[1],
            'description': event[4],
            'poster': event[3],
            'time': event[2]
        }
        events_dict.append(m)
    return events_dict

def apply_for_event(user_name, event_id):
    conn = sqlite3.connect('datubazes.db')
    cursor = conn.cursor()
    
    # First get the user's ID
    cursor.execute('SELECT id FROM users WHERE name = ?', (user_name,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return False
    
    user_id = user[0]
    
    # Check if already registered
    cursor.execute('SELECT * FROM pieteikties WHERE user_id = ? AND event_id = ?', (user_id, event_id))
    if cursor.fetchone():
        conn.close()
        return False
    
    # Register for event
    cursor.execute('INSERT INTO pieteikties (user_id, event_id) VALUES (?, ?)', (user_id, event_id))
    conn.commit()
    conn.close()
    return True

def get_event_participants(event_id=None):
    conn = sqlite3.connect('datubazes.db')
    cursor = conn.cursor()
    
    if event_id:
        # Get participants for a specific event
        cursor.execute('''
            SELECT users.name, users.surname, users.class 
            FROM pieteikties 
            JOIN users ON pieteikties.user_id = users.id 
            WHERE pieteikties.event_id = ?
        ''', (event_id,))
    else:
        # Get all participants for all events
        cursor.execute('''
            SELECT users.name, users.surname, users.class, events.title 
            FROM pieteikties 
            JOIN users ON pieteikties.user_id = users.id 
            JOIN events ON pieteikties.event_id = events.id
        ''')
    
    participants = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    participants_list = []
    for participant in participants:
        if event_id:
            participants_list.append({
                'name': participant[0],
                'surname': participant[1],
                'class': participant[2]
            })
        else:
            participants_list.append({
                'name': participant[0],
                'surname': participant[1],
                'class': participant[2],
                'event': participant[3]
            })
    
    return participants_list

if __name__ == "__main__":
    create_datubazi()
