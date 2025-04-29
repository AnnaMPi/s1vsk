import sqlite3
def drop_datubazi():
    conn = sqlite3.connect("datubazes.db")
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS events''')
    conn.commit()
    cursor.execute('''DROP TABLE IF EXISTS users''')
    conn.commit()
    conn.close()

def create_datubazi():
    conn = sqlite3.connect("datubazes.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   title TEXT,
                   time TEXT,
                   poster TEXT,
                   description TEXT)''')
    
    conn.commit()
    cursor.execute('''INSERT INTO events VALUES(1, "1.aprīls", "16:00, 1.04.2025", 'https://www.ozolniekuvsk.lv/wp-content/uploads/2022/03/aprilis.png', 'descrition')''')
    conn.commit()
    cursor.execute('''INSERT INTO events VALUES(2, "Eko diena", "14:00, 27.05.2025",'https://kekava.lv/wp-content/uploads/2023/04/Majaslapas-titulslaids18.png', 'descroriptoion')''')
    conn.commit()
    
    # cursor.execute('''INSERT INTO events VALUES(3, "Eko diena", "14:00, 27.05.2025",'https://kekava.lv/wp-content/uploads/2023/04/Majaslapas-titulslaids18.png', 'descroriptoion')''')
    # conn.commit()
    
    # cursor.execute('''INSERT INTO events VALUES(4, "Eko diena", "14:00, 27.05.2025",'https://kekava.lv/wp-content/uploads/2023/04/Majaslapas-titulslaids18.png', 'descroriptoion')''')
    # conn.commit()
    
    # cursor.execute('''INSERT INTO events VALUES(5, "Eko diena", "14:00, 27.05.2025",'https://kekava.lv/wp-content/uploads/2023/04/Majaslapas-titulslaids18.png', 'descroriptoion')''')
    # conn.commit()

    
    # cursor.execute('''INSERT INTO events VALUES(3, "Krepkij Ore6ek", '["10:00", "12:00", "16:00", "20:00"]','https://via.placeholder.com/200x300?text=Крепкий+орешек', 'Фильм про орешек')''')
    # conn.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   name TEXT,
                   surname TEXT,
                   password TEXT,
                   class TEXT,
                   role TEXT)''')
    conn.commit()
    
    cursor.execute('''insert into users values(0, "Teacher", "Teacher", "Teacher", "0", "Admin")''')
    conn.commit()   
    conn.close()

def register_user(vards, uzvards, parole, klase):
    print("Reģistrācija")
    conn = sqlite3.connect('datubazes.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, surname, password, class, role) VALUES (?, ?, ?, ?, "Student")', (vards, uzvards, parole, klase))
    conn.commit()
    users_id = c.lastrowid  # Get the auto-generated id
    conn.close()
    print("Reģistrācija beidzās")
    return users_id
    
def get_user(name, surname, password):
    print("Логин")
    conn = sqlite3.connect('datubazes.db')  # Use the correct database file
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name = ? AND surname = ? AND password = ?"
    cursor.execute(query, (name, surname, password))
    users = cursor.fetchone()
    conn.close()
    print(users)
    return users  # Returns None if no user is found

def get_events():
    conn = sqlite3.connect("datubazes.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM events''')
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
    print(events_dict)
    return events_dict

def get_events_by_date(date_str):
    conn = sqlite3.connect("datubazes.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM events WHERE time LIKE ?''', (f'%{date_str}%',))
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

if __name__ == "__main__":
    create_datubazi()
