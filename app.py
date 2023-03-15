from flask import Flask, render_template, url_for, request, flash, redirect, session, abort


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


# Перенаправление запроса (пользователь в браузере логинится-если успешно, 
# то он перенаправляется на новую страницу 
# или пользователь был залогинен и заходит снова, то второй раз, 
# страницу с формой не нужно отображать, делаю сразу переадресацию в профаил)
@app.route("/login", methods=["POST", "GET"])
def login():
    # Если св-во "userLogged" существует в сесии, то происходит переадресация на соответствующий профаил, с тем username, который находится в ссесии
    if "userLogged" in session:
        return redirect(url_for("profile", username=session["userLogged"]))
    
    # А иначе, берутся данные из формы, если они соответ-ют ["username"] == "admin" и паролю == "123", 
    # то сохраняются данные в ссесии и делается переадресация
    elif request.method == 'POST' and request.form["username"] == "admin" and request.form["psw"] == "123":
        session["userLogged"] = request.form["username"]
        return redirect(url_for("profile", username=session["userLogged"]))
    
    # Если все выше не проходит, отображаю данные формы
    return render_template("login.html", title="Авторизация", menu=menu)

# Профайл пользователя (если он залогинен) или вывод 401
@app.route("/profile/<username>")
def profile(username):

    # Проверка. Если пользователь самостоятельно набират како то путь (чужой профаил), то ему нельзя давать доступ к этому профайлу
    # Если пользователь не залогинился или св-во в ссесии не соответствует username, возвращаю ошибку сервера
    if "userLogged" not in session or session["userLogged"] != username:
        abort(401)

    return f"Профиль пользователя: {username}"


# Обработка ошибок (неправильно введенный адрес) 
@app.errorhandler(404)
def pageNotFound(error):
    return render_template("page404.html", title="Страница не найдена", menu=menu)

    # # Если все таки требуется возвращать 404
    # return render_template("page404.html", title="Страница не найдена", menu=menu), 404





# Динамические url-адрес. Принимает username (/profile/Artem)
@app.route("/profile1/<username>")
def profile1(username):
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

