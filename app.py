from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

db = SQLAlchemy()
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
# app.secret_key = "hello"
# db.init_app(app)
# app.permanent_session_lifetime = timedelta(minutes=5)



def create_app():
    app1 = Flask(__name__)
    app1.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
    app1.config['SECRET_KEY'] = "random string"
    db.init_app(app1)
    app1.permanent_session_lifetime = timedelta(minutes=5)
    return app1


class Hotels(db.Model):
    hotel_name = db.Column(db.String(100), primary_key=True)
    rooms_available = db.Column(db.Integer)

    def __init__(self, name, num_rooms):
        self.hotel_name = name
        self.rooms_available = num_rooms


class Customers(db.Model):
    name = db.Column('Customer name', db.String, primary_key=True)
    email = db.Column('Customer email', db.String(50))
    room_id = db.Column('Room id', db.String(200))

    def __init__(self, name, email, room_id):
        self.name = name
        self.email = email
        self.room_id = room_id


class Rooms(db.Model):
    number = db.Column(db.Integer)
    type = db.Column(db.String(100))
    hotel_name = db.Column(db.String(100))
    room_id = db.Column(db.String, primary_key=True)
    Availability = db.Column(db.Integer)
    Price = db.Column(db.Integer)

    def __init__(self, num, room_type, h_name, r_id, avail, r_price):
        self.number = num
        self.type = room_type
        self.hotel_name = h_name
        self.room_id = r_id
        self.Availability = avail
        self.Price = r_price


def addhotels():
    if db.session.query(Hotels).count() <= 1:
        hotel1 = Hotels("Hilton Hotel", 5)
        db.session.add(hotel1)
        db.session.commit()
        hotel2 = Hotels("Villa Italia South Beach Miami", 5)
        db.session.add(hotel2)
        db.session.commit()
        hotel3 = Hotels("Cambria Hotel", 5)
        db.session.add(hotel3)
        db.session.commit()
        hotel4 = Hotels("Good time hotel", 5)
        db.session.add(hotel4)
        db.session.commit()
        hotel5 = Hotels("demo hotel", 5)
        db.session.add(hotel5)
        db.session.commit()


def addrooms():
    roomtype = ["Double", "Double", "Quad", "Quad", "Presidential"]
    roomprice = [100, 100, 200, 200, 500]
    a = []
    for i in range(0, 5):
        id_room = "HH" + str(i)
        a.append(id_room)

    b = []
    for i in range(0, 5):
        id_room = "VH" + str(i)
        b.append(id_room)

    c = []
    for i in range(0, 5):
        id_room = "CH" + str(i)
        c.append(id_room)

    d = []
    for i in range(0, 5):
        id_room = "CH" + str(i)
        d.append(id_room)

    if db.session.query(Rooms).count() <= 1:
        j = 0
        for i in a:
            temp_room = Rooms(j, roomtype[j], "Hilton Hotel", i, 1, roomprice[j])
            db.session.add(temp_room)
            db.session.commit()
            j = j + 1

        j = 0
        for i in b:
            temp_room = Rooms(j, roomtype[j], "Villa Italia South Beach Miami", i, 1, roomprice[j])
            db.session.add(temp_room)
            db.session.commit()
            j = j + 1

        j = 0
        for i in c:
            temp_room = Rooms(j, roomtype[j], "Cambria Hotel", i, 1, roomprice[j])
            db.session.add(temp_room)
            db.session.commit()
            j = j + 1


# returns the total rooms of a given hotel
def getAllHotelRooms(hotelname):
    total_rooms = Hotels.query.filter_by(hotel_name=hotelname).all()
    return total_rooms[0].rooms_available


# returns the room id
def get_room_id(hotelname, r_type):
    total_rooms = db.session.query(Rooms).with_entities(Rooms.room_id).filter(Rooms.hotel_name.like(hotelname),
                                                                              Rooms.type.like(r_type),
                                                                              Rooms.Availability > 0).first()
    return total_rooms[0]
# returns the total rooms of a type of room of a hotel
def getSpecificRooms(hotelname, r_type):
    total_rooms = db.session.query(Rooms).with_entities(Rooms.room_id).filter(Rooms.hotel_name.like(hotelname),
                                                                              Rooms.type.like(r_type),
                                                                              Rooms.Availability > 0).all()

    return(len(total_rooms))
    # for hotel in total_rooms:
    #     print(hotel.room_id)


def updateRooms(r_id):
    thisRoom = Rooms.query.filter_by(room_id=r_id).first()
    thisRoom.Availability = 0
    db.session.commit()
    # print(thisRoom.Availability)

    temp_name = thisRoom.hotel_name
    hoteldata = Hotels.query.filter_by(hotel_name=temp_name).first()
    availableRooms = Hotels.query.with_entities(Hotels.rooms_available).filter(
        Hotels.hotel_name.like(temp_name)).first()
    newNumber = availableRooms.rooms_available - 1
    hoteldata.rooms_available = newNumber
    db.session.commit()
    print(hoteldata.rooms_available)


# book a room for a specific customer
def booking(c_name, c_email, r_id):
    newCustomer = Customers(c_name, c_email, r_id)
    db.session.add(newCustomer)
    db.session.commit()
    updateRooms(r_id)


def getCustomer(cname):
    customerdata = Customers.query.filter_by(name=cname).first()
    return customerdata


def getRoomType(r_id):
    thisRoom = Rooms.query.filter_by(room_id=r_id).first()
    return thisRoom.type


def getHotelName(r_id):
    thisRoom = Rooms.query.filter_by(room_id=r_id).first()
    return thisRoom.hotel_name


app = create_app()
app.app_context().push()
db.drop_all()
db.create_all()
addhotels()
addrooms()


# WEB PAGE BEGINS
@app.route('/', methods=["GET", "POST"])
def home():
    # querying rooms
    hilton = getAllHotelRooms("Hilton Hotel")
    villa = getAllHotelRooms("Villa Italia South Beach Miami")
    cambria = getAllHotelRooms("Cambria Hotel")
    good_time = getAllHotelRooms("Good time hotel")
    if request.method == "POST":
        session.permanent = True
        hotel_name = request.form["hotel"]
        session["hotel_name"] = hotel_name
        return redirect(url_for("available"))
    return render_template('register.html', h_room=hilton, g_room=good_time, c_room=cambria, v_room=villa)


@app.route('/available', methods=["GET", "POST"])
def available():  # put application's code here
    if request.method == "POST":
        selected_room = request.form.get("ROOM_TYPE")
        session['selected_room'] = selected_room
        return redirect(url_for("customer"))

    # query the rooms available and put here
    rooms_double_t = getSpecificRooms(session['hotel_name'], 'Double')
    rooms_quad_t = getSpecificRooms(session['hotel_name'], 'Quad')
    rooms_pres_t = getSpecificRooms(session['hotel_name'], 'Presidential')
    return render_template('available.html', rooms_double=rooms_double_t, rooms_quad=rooms_quad_t, rooms_pres=rooms_pres_t)


@app.route('/customer', methods=["GET", "POST"])
def customer():  # put application's code here
    if request.method == "POST":
        name = request.form.get("customer_name")
        email = request.form.get("Email")
        session['name'] = name
        session['email'] = email
        booking(session['name'], session['email'], get_room_id(session['hotel_name'], session['selected_room']))

        return redirect(url_for("check"))
    return render_template('customer.html')


@app.route('/customer_check', methods=["GET", "POST"])
def customer_check():  # put application's code here
    if request.method == "POST":
        name = request.form.get("customer_name")
        email = request.form.get("Email")
        session['name'] = name
        session['email'] = email
        return redirect(url_for("check"))
    return render_template('customer.html')


@app.route('/logout')
def logout():
    session.pop('hotel_name')
    session.pop('selected_room')
    session.pop('name')
    session.pop('email')

    return redirect(url_for("home"))

@app.route('/checkbooking')
def check():
    c_data = getCustomer(session['name'])
    hotel = getHotelName(c_data.room_id)
    r_type = getRoomType(c_data.room_id)


    return render_template("checkbooking.html", c_name=c_data.name, email=c_data.email,hotel=hotel,r_type=r_type,rm_id=c_data.room_id)
if __name__ == '__main__':
    app.static_folder = 'static'
    app.run(debug=True)
