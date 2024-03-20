from website import app, db
from flask import render_template
from website.models import User
  # CONFIG 

app = app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/browse')  # TODO move this into a separate file
def browse():
    return render_template('browse.html')

def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(User(firstname="admin", lastname="admin", email='admin@test.com', password='Password1!', role="admin"))
    db.session.add(User(firstname="user", lastname="user", email='user@test.com', password='Password1!', role="user"))
    db.session.add(User(firstname="venue", lastname="venue", email='venue@test.com', password='Password1!', role='venue'))
    db.session.commit()


if __name__ == '__main__':
    
    
    from website.users.views import users_blueprint
    from website.admin.views import admin_blueprint 
    from website.venue.views import venue_blueprint
    
    
    app.register_blueprint(users_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(venue_blueprint)
    
    with app.app_context():
        db.create_all()
    
    app.run(host="127.0.0.1", port="38255", debug=True)