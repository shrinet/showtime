import time, datetime, json
from flask import jsonify, Blueprint, request, make_response, url_for
from flask_restful import Api, Resource
from flask_security import auth_required, auth_token_required
from flask_login import login_user, logout_user, current_user
from functools import wraps
from app.models import User, Show, Booking
from app import db, cache
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt
from flask_cors import cross_origin
from flask_caching import CachedResponse

import app.config

bp = Blueprint('api', __name__)
api = Api(prefix=app.config.API_PREFIX)


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper



class DataProcessingAPI(Resource):
    @auth_required('token')
    def post(self):
        task = process_data.delay()
        return {'task_id': task.id}, 200
    
    #@auth_required('token')
    def get(self):
        return {'result': 'ok'}, 200


class RegistrationApi(Resource):
    @cross_origin(supports_credentials=True)
    def post(self):
        body = request.get_json()
        
        user = User(username=body['username'], email=body['email'])
        user.set_password(body['password'])
        db.session.add(user)
        db.session.commit()
        id = user.id
        return {'id': str(id)}, 200


class LoginApi(Resource):
    @cross_origin(supports_credentials=True)
    def post(self):
        if current_user.is_authenticated:
            return {'error': 'you already logged in'}, 200
        body = request.get_json()
        user = User.query.filter_by(username=body.get('username')).first()
        if user is None or not user.check_password(body.get('password')):
            return {'error': 'Email or password invalid'}, 401
        login_user(user, remember=True)
        
        expires = datetime.timedelta(days=7)
        if(user.isAdmin):
            access_token = create_access_token("admin_user", additional_claims={"is_administrator": True}, expires_delta=expires)
        else:
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        
        return {'username': user.isAdmin, 'token': access_token}, 200
    

class MoviesApi(Resource):
    @cache.cached()
    def get(self):
        page = request.args.get('page', 1, type=int)
        #shows = Show.query.all()
        try:
            shows = Show.query.all()
            return CachedResponse(make_response(jsonify([show.json() for show in shows]), 200),timeout=150)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


class MovieApi(Resource):
    def get(self, show_id):
        show = Show.query.filter_by(id=show_id).first()
        return make_response(jsonify(show.json()), 200)
    

class HallApi(Resource):
    def get(self, show_id, showtime):
        show = Show.query.filter_by(id=show_id).first()
        bsheats = Booking.query.with_entities(Booking.sheats).filter_by(show_id=show_id, showTime=showtime).all()
        booked_sheat = list()
        for bsheat in bsheats:
            for i in bsheat:
                booked_sheat.append(i)
            
        booked_sheat = [int(item) for items in booked_sheat for item in items.split(",")]
        
        return make_response(jsonify({'show': show.json(),'booked': booked_sheat}), 200) 


class BookingApi(Resource):
    @cross_origin(supports_credentials=True)
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        body = request.get_json()
        y = json.loads(body.get('seats'))
        print(y)
        booking = Booking(date=body.get('date'), show_id=body.get('show_id'),
                      sheats=body.get('seats').replace('[','').replace(']','') ,price=body.get('price'),showTime=body.get('showTime'),
                      user_id=current_user)
        db.session.add(booking)
        db.session.commit()
        return make_response(jsonify({'id':89 }), 200)     

class LogoutApi(Resource):
    def get(self):
        if current_user.is_authenticated:
            logout_user()
        return { 'success': 'Done'}  
    


class AdminDashboardApi(Resource):
    @admin_required()
    def get(self):
        return {'success': 'Done'}      
    
class AdminShowApi(Resource):
    @admin_required()
    def get(self):
        shows = Show.query.all()
        return make_response(jsonify([show.json() for show in shows]), 200)   

# Registration endpoint
api.add_resource(RegistrationApi, '/register')

# Login endpoint

api.add_resource(LoginApi, '/login')

# Logout endpoint
api.add_resource(LogoutApi, '/logout')

api.add_resource(MoviesApi, '/movies')

api.add_resource(MovieApi, '/movie/<int:show_id>')

api.add_resource(HallApi, '/hall/<int:show_id>/<showtime>')

api.add_resource(BookingApi, '/booking')


api.add_resource(AdminDashboardApi, '/admin/dashboard')
api.add_resource(AdminShowApi, '/admin/show')


