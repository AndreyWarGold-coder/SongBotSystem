from flask import Flask, jsonify, request
import classes

#flask --app FlaskStartFile run


app = Flask(__name__)
controller = classes.CommandController()


def is_token(token: str):
    return token == "dcjHdslJ63ndjGDLKdkskl37smw93jnc83dnj"

@app.route("/", methods=['GET'])
def hello_world():
    return "Hello, World!"

@app.route("/get_token", methods=['POST'])
def get_token():
    if(request.form['login'] == "AndreyWarGold" and request.form['password'] == "ZalupaNegra"):
        return jsonify("dcjHdslJ63ndjGDLKdkskl37smw93jnc83dnj"), 200
    return jsonify("None access"), 403

@app.route("/start_game_standart", methods=['POST'])
def start_standart():
    token = request.form['token']
    if not is_token(token):
        return jsonify(None), 403
    author = request.form['author']
    author_id = request.form['author_id']
    chat_id = request.form['chat_id']
    messanger = request.form['messanger']
    return jsonify(controller.start_defoult_mode(chat_id, author, messanger))

@app.route("/start_game_up_down", methods=['POST'])
def start_up_down():
    token = request.form['token']
    if not is_token(token):
        return jsonify(None), 403
    author = request.form['author']
    author_id = request.form['author_id']
    chat_id = request.form['chat_id']
    messanger = request.form['messanger']
    return jsonify(controller.start_UpDown_mode(chat_id, author, messanger))

@app.route("/clk_btn", methods=['POST'])
def clk_btn():
    token = request.form['token']
    if not is_token(token):
        return jsonify(None), 403
    author = request.form['author']
    author_id = request.form['author_id']
    chat_id = request.form['chat_id']
    messanger = request.form['messanger']
    text = request.form['text']
    return jsonify(controller.click_button(text, chat_id, author, author_id, messanger))


@app.route("/text_command", methods=['POST'])
def text_command():
    token = request.form['token']
    if not is_token(token):
        return jsonify(None), 403
    author = request.form['author']
    author_id = request.form['author_id']
    chat_id = request.form['chat_id']
    messanger = request.form['messanger']
    text = request.form['text']
    return jsonify(controller.command_text(text, chat_id, author, author_id, messanger))

@app.route("/end", methods=['POST'])
def text_command():
    token = request.form['token']
    if not is_token(token):
        return jsonify(None), 403
    author = request.form['author']
    author_id = request.form['author_id']
    chat_id = request.form['chat_id']
    messanger = request.form['messanger']
    return jsonify(controller.end_session(chat_id, author, author_id, messanger))