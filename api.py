from flask_restful import Resource, fields, marshal_with, reqparse
from models import Venue, Show
from validation import NotFoundError, BusinessValidationError
from models import db

venue_fields = {
    'venueid': fields.Integer,
    'name': fields.String,
    'place': fields.String,
    'capacity': fields.String
}

venue_parser = reqparse.RequestParser()
venue_parser.add_argument('name')
venue_parser.add_argument('place')
venue_parser.add_argument('capacity')

class VenueAPI(Resource):
    @marshal_with(venue_fields)

    def get(self, venueid1):
        l = Venue.query.get(venueid1)
        return l

    @marshal_with(venue_fields)
    def post(self, venueid):
        
        args = venue_parser.parse_args()
        name = args.get('name', None)
        place = args.get('place', None)
        capacity = args.get('capacity', None)

        l = Venue.query.filter_by(name=name,venueid=venueid).first()
        if l is not None:
            raise BusinessValidationError(status_code=400, error_code='Venue002', error_message='Venue Name already exists')
        
        l = Venue(venueid=venueid, name=name, place=place, capacity=capacity)
        db.session.add(l)
        db.session.commit()
        return l, 201

    def delete(self, venueid):
        l = Venue.query.get(venueid)
        if l is None:
            raise NotFoundError(status_code=404)
        else:
            db.session.delete(l)
            db.session.commit()
            return "Successfully Deleted"

    @marshal_with(venue_fields)
    def put(self, venueid):
        l = Venue.query.get(venueid)
        if l is None:
            raise NotFoundError(status_code=404)

        args = venue_parser.parse_args()
        name = args.get('name', None)
        place = args.get('place', None)
        capacity = args.get('capacity', None)

        if name is None:
            raise BusinessValidationError(status_code=400, error_code='Venue001', error_message='Venue Name is required')

        new = Venue.query.filter_by(name=name,venueid=l.venueid).first()
        if l.name == name or new == None:
            l.name = name
            l.place = place
            l.capacity = capacity
            db.session.commit()
            return l,200
        else:
            raise BusinessValidationError(status_code=400, error_code='Venue002', error_message='Venue Name already exists')



show_fields = {
    'showid': fields.Integer,
    'showname': fields.String,
    'rating': fields.Integer,
    'tag': fields.String,
    'price': fields.Integer,
    'showcapacity': fields.Integer,
    'eshowid': fields.Integer
}

show_parser = reqparse.RequestParser()
show_parser.add_argument('showname')
show_parser.add_argument('rating')
show_parser.add_argument('tag')
show_parser.add_argument('price')
show_parser.add_argument('showcapacity')

class ShowAPI(Resource):
    @marshal_with(show_fields)
    def get(self, showid):
        l = Show.query.get(showid)
        return l

    @marshal_with(show_fields)
    def post(self, showid):
        args = show_parser.parse_args()
        showname = args.get('showname', None)
        rating = args.get('rating', None)
        tag = args.get('tag', None)
        price = args.get('price', None)
        showcapacity = args.get('showcapacity', None)

        if showname is None:
            raise BusinessValidationError(status_code=400, error_code='SHOW001', error_message='Show Name is required')

        
        c = Show(showid=showid,showname=showname, rating=rating, tag=tag, price=price, showcapacity=showcapacity)
        db.session.add(c)
        db.session.commit()
        return c, 201

    def delete(self, showid):
        show = Show.query.get(showid)
        if show is None:
            raise NotFoundError(status_code=404)
        else:
            db.session.delete(show)
            db.session.commit()
            return "Successfully Deleted"

    @marshal_with(show_fields)
    def put(self, showid):
        show = Show.query.get(showid)
        if show is None:
            raise NotFoundError(status_code=404)

        args = show_parser.parse_args()
        showname = args.get('showname', None)
        rating = args.get('rating', None)
        tag = args.get('tag', None)
        price = args.get('price', None)
        showcapacity = args.get('showcapacity', None)
        eshowid = args.get('eshowid', None)

        l = Show.query.get(showid)
        if l is None:
            raise NotFoundError(status_code=404)

        c = Show.query.filter_by(showname=showname,showid=showid).first()

        flag = False
        if show.showid == showid:
            if show.showname == showname or c == None:
                flag = True
        elif c == None:
            show.showid = showid
            flag = True
        
        if flag:
            show.showname = showname
            show.rating = rating
            show.tag = tag
            show.price = price
            show.showcapacity = showcapacity
            db.session.commit()
            return show,200
        else:
            raise BusinessValidationError(status_code=400, error_code='SHOW004', error_message='Show Name already exists in the given list')