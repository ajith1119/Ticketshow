from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_restful import Api
from models import User, Venue, Show, Ticket, db
from database import app
from api import VenueAPI, ShowAPI


api = Api(app)

api.add_resource(VenueAPI, "/api/venues/<venueid1>", "/api/createvenue/<venueid>", "/api/deletevenue/<venueid>", "/api/updatevenue/<venueid>")
api.add_resource(ShowAPI, "/api/shows/<showid>", "/api/createshow/<showid>", "/api/deleteshow/<showid>", "/api/updateshow/<showid>")

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user)

        venues = Venue.query.all()

        return render_template('venue.html', venues=venues, venue=current_user, user=current_user)

    return render_template('login.html', user=current_user)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('signup'))

        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user=current_user)



@app.route('/addvenue',methods=['GET','POST'])
def addvenue():

    if request.method == 'GET':
        return render_template('addvenue.html', user = current_user)
    
    elif request.method == 'POST':

        data = Venue(name=request.form['name'], place=request.form['place'], capacity=request.form['capacity'])

        db.session.add(data)

        db.session.commit()

        venue = Venue.query.filter_by(name = request.form['name']).first()

        venues = Venue.query.all()

    return render_template('venue.html',venue=venue, venues=venues, user=current_user)



@app.route('/addvenue/<int:venueid>/edit',methods=['GET','POST'])
def editvenue(venueid):
    
   venue = Venue.query.filter_by(venueid=venueid).first()

   if request.method == 'GET':
      return render_template('editvenue.html',venue=venue, user=current_user)


   elif request.method == 'POST':
      lid = venue.venueid
      db.session.delete(venue)
      up = Venue(venueid=lid,name=request.form['name'], place=request.form['place'], capacity=request.form['capacity'])
      db.session.add(up)

      db.session.commit()

      venue = Venue.query.filter_by(venueid=venueid).first()

      venues = Venue.query.all()

      return render_template('venue.html',venue=venue, venues=venues, user=current_user)
   


@app.route('/addvenue/<int:venueid>/delete',methods=['GET','POST'])
def deletevenue(venueid):

   venueid = Venue.query.filter_by(venueid=venueid).first()

   db.session.delete(venueid)
   db.session.commit()
   
   venues = Venue.query.all()

   return render_template('venue.html',venue=current_user, venues=venues, user=current_user)


@app.route('/deleteallvenues',methods=['GET','POST'])

def deleteallvenues():

    if request.method == 'POST':
        
        Venue.query.filter(Venue.venueid > 0).delete()

        db.session.commit()

    venues = Venue.query.all()

    return render_template('venue.html',venue=current_user, venues=venues,user=current_user)



@app.route('/addshow/<int:venueid>',methods=['GET','POST'])
def addshow(venueid):

    poster = venueid

    venue = Venue.query.filter_by(venueid=venueid).first()

    if request.method == 'GET':
        return render_template('addshow.html', venue=venue, user = current_user)
    
    elif request.method == 'POST':

        data = Show(showname=request.form['showname'], rating=request.form['rating'], tag=request.form['tag'], price=request.form['price'], showcapacity=request.form['showcapacity'], eshowid = poster)

        db.session.add(data)

        db.session.commit()

        show = Show.query.filter_by(eshowid = poster).first()

        shows = Show.query.all()

    return render_template('show.html',show=show, shows=shows, venue=venue , user=current_user)


@app.route('/addshow/<int:venueid>/<int:showid>/edit',methods=['GET','POST'])
def editshow(venueid, showid):
    
   venue = Venue.query.filter_by(venueid=venueid).first()

   show = Show.query.filter_by(showid=showid).first()

   poster = venueid

   if request.method == 'GET':
      return render_template('editshow.html',venue=venue, show=show, user=current_user)


   elif request.method == 'POST':
      sid = show.showid
      poster = show.eshowid
      db.session.delete(show)
      up = Show(showid=sid,showname=request.form['showname'], rating=request.form['rating'],tag=request.form['tag'], price=request.form['price'], showcapacity=request.form['showcapacity'], eshowid = poster)
      db.session.add(up)

      db.session.commit()

      venue = Venue.query.filter_by(venueid=venueid).first()

      shows = Show.query.all()

      return render_template('show.html',show=current_user, shows=shows,venue=venue, user=current_user)
   


@app.route('/addshow/<int:venueid>/<int:showid>/delete',methods=['GET','POST'])
def deleteshow(venueid, showid):

   venue = Venue.query.filter_by(venueid=venueid).first()

   showid = Show.query.filter_by(showid=showid).first()

   db.session.delete(showid)
   db.session.commit()

   shows = Show.query.all()

   return render_template('show.html',venue=venue, show = current_user, shows=shows, user=current_user)

@app.route('/displayshow/<int:venueid>',methods=['GET','POST'])
def displayshow(venueid):

   venue = Venue.query.filter_by(venueid=venueid).first()

   shows = Show.query.all()

   return render_template('show.html',venue=venue, show = current_user, shows=shows,user=current_user)



@app.route('/ticket/<int:id>/<int:venueid>/<int:showid>',methods=['GET','POST'])
def ticket(id,venueid, showid):

    poster = showid
    
    post = id

    venue = Venue.query.filter_by(venueid=venueid).first()

    show = Show.query.filter_by(showid=showid).first()


    if request.method == 'GET':
        return render_template('bookticket.html', venue=venue,show=show, user = current_user)
    
    elif request.method == 'POST':

        ava = show.showcapacity

        if (ava < int(request.form['nooftickets'])):
                
            return render_template('ticketshow.html',show=show, venue=venue, message="Booking Failed..... because entered more than show capacity", user=current_user)

        else:
            
            show.showcapacity -= int(request.form['nooftickets'])

            data = Ticket(name=request.form['personname'], email=request.form['email'], phoneno=request.form['phoneno'], nooftickets=request.form['nooftickets'], eticketid=poster, euserid=post)

            db.session.add(data)

            db.session.commit()

            ticket = Ticket.query.filter_by(eticketid = poster).first()

            shows = Show.query.all()

            tickets = Ticket.query.all()

        return render_template('ticketshow.html',show=show, shows=shows, venue=venue, ticket=ticket, tickets=tickets, user = current_user)



@app.route('/search',methods=['GET','POST'])
def search():
    
    if request.method == 'POST':

        place=request.form['search']

        venue = Venue.query.filter_by(place=place).first()

        venues = Venue.query.filter_by(place=place).all()

    return render_template('venue.html',venue=venue, venues=venues, user=current_user)

@app.route('/showsearch',methods=['GET','POST'])
def showsearch():
    
    if request.method == 'POST':

        tag = request.form['search']

        show = Show.query.filter_by(tag=tag).first()

        shows = Show.query.filter_by(tag=tag).all()

        venues = Venue.query.all()

        return render_template('showsearch.html', show=show, shows=shows, user=current_user, venue= current_user, venues=venues)

@app.route('/venuedisplay',methods=['GET','POST'])
def venuedisplay():

    venues = Venue.query.all()

    return render_template('venue.html',venue=current_user,venues=venues, user = current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



if __name__ == '__main__':
  # Run the Flask app
  app.run(debug=True, host='127.0.0.1',port=8000)
