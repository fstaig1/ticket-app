from website import app
from flask import render_template
  # CONFIG 

app = app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/browse')  # TODO move this into a separate file
def browse():
    return render_template('browse.html')




if __name__ == '__main__':
    
    
    from website.users.views import users_blueprint
    from website.admin.views import admin_blueprint 
    from website.venue.views import venue_blueprint
    
    
    app.register_blueprint(users_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(venue_blueprint)
    
    
    app.run(host="127.0.0.1", port="38255", debug=True)