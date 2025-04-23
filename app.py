from flask import Flask, render_template, request, redirect, url_for
import datub

datub.drop_datubazi()
app = Flask(__name__)
datub.create_datubazi()

@app.route('/')
def index():
    movies = datub.take_info()
    return render_template('index.html', movies=movies)

@app.route('/movies')
def movie_list():
    movies = datub.take_info()
    return render_template('movies.html', movies=movies)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movies = datub.take_info()
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if not movie:
        return "Фильм не найден", 404
    return render_template('movie.html', movie=movie)

@app.route('/book/<int:movie_id>', methods=['GET', 'POST'])
def book_ticket(movie_id):
    movies = datub.take_info()
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if not movie:
        return "Фильм не найден", 404
    
    if request.method == 'POST':
        # Обработка данных формы
        name = request.form.get('name')
        email = request.form.get('email')
        showtime = request.form.get('showtime')
        seats = request.form.get('seats')
        
        # Здесь должна быть логика сохранения бронирования (в реальном приложении)
        print(f"Бронирование: {name}, {email}, {movie['title']}, {showtime}, мест: {seats}")
        
        return redirect(url_for('booking_success'))
    
    return render_template('booking.html', movie=movie)

@app.route('/booking/success')
def booking_success():
    return "Бронирование успешно завершено! Спасибо за покупку."

if __name__ == '__main__':
    app.run(debug=True)
