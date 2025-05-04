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

def apply_for_event(user_id, event_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(""" INSERT INTO pieteikties (user_id, event_id) VALUES (?, ?) """, (user_id, event_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_datubazi()
