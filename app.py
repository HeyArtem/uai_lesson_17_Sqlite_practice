from flask import Flask, render_template, url_for, request, flash


app = Flask(__name__)

# секретный ключ необходим для работы ссесии (здесь используется для работы с мгновенными сообщениями)
app.config["SECRET_KEY"] = "asdf;lkjasdf;lkj"

# menu = ["Установка", "Первое приложение", "Обратная связь", ]

menu = [
    {"name": "Установка", "url": "install-flask"},
    {"name": "Первое приложение", "url": "first-app"},
    {"name": "Обратная связь", "url": "contact"}
    ]


@app.route("/index")
@app.route("/")
def index():
    # Функция url_for, работает только в контексте запроса. Вывод в консоль url. Если декораторов много, выведется ближайший (конкретно здесь '/')
    print(url_for("index"))
    return render_template("index.html", menu=menu)


@app.route("/about")
def about():
    print(url_for("/about"))
    return render_template("about.html", title="О сайте", menu=menu)


# Форма обратная связь, отправка мгновенного сообщения
@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":

        # Проверка данных из формы, отправка сообщения
        if len(request.form["username"]) > 2:
            flash("Сообщение отправлено", category="success")
        else:
            flash("Ошибка отправки сообщения", category="error")


        # В терминал распечатываю данные из формы
        print(request.form)
        print(request.form["username"])
        print(request.form["email"])
        print(request.form["message"])
    
    return render_template("contact.html", title="Обратная связь", menu=menu)




# Динамические url-адрес. Принимает username (/profile/Artem)
@app.route("/profile/<username>")
def profile(username):
    print(url_for("profile", username="username"))
    return f"Пользователь: {username}"


# Динамические url-адрес. Конвертер "path". Принимает ВСЕ посте username path (/profile2/Artem/123)
@app.route("/profile2/<path:username>")
def profile2(username):    
    return f"Пользователь: {username}<hr> int - только цифры <br> float - можно цифры с плавающей запятой <br> path - можно использовать любые допустимые символы URL плюс символ '/'. "


# Динамические url-адрес. Принимает int (/profile3/123)
@app.route("/profile3/<int:username>")
def profile3(username):    
    return f"Пользователь: {username}"


# Динамические url-адрес. Принимает ДВЕ переменных (http://127.0.0.1:5000/profile4/123/Art)
@app.route("/profile4/<int:username>/<path>")
def profile4(username, path):    
    return f"Пользователь: {username}, {path}"











if __name__ == "__main__":
    # запуск локального web-сервера
    app.run(debug=True)

