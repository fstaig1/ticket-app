import socket
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

  # CONFIG 
app = Flask(__name__)
app.config['SECRET_KEY'] = '6LfaX9ocAAAAABWeVBjjXEZTI5tmcxVkO0fDi32J'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/browse')
def browse():
    return render_template('browse.html')


if __name__ == '__main__':
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()

    # BLUEPRINTS
    from users.views import users_blueprint
    from admin.views import admin_blueprint
    from venue.views import venue_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(venue_blueprint)
    
    app.run(host=my_host, port=free_port, debug=True)
