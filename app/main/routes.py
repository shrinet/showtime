import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app import db, admin
from functools import wraps
from app.main.forms import EditProfileForm, EmptyForm, VenueForm, ShowForm, BookingForm, ImageUploadForm, ReviewForm
from app.models import User, Venue, Show, Rating, Booking, Images
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import secure_filename
from app.main import bp
import app
import uuid


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    

# admin management setup
admin.add_view(ModelView(User, db.session))
#admin.add_view(ModelView(Post, db.session))

def requires_admin(f):
    """Checks if user has admin access"""
    @wraps(f)
    def wrapped(*arg, **kwargs):
        if current_user.isAdmin:
            return f(*arg, **kwargs)
        flash('You dont have admin access')
        return redirect(url_for('main.index'))
    return wrapped


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET'])
@login_required
def index():
    
    page = request.args.get('page', 1, type=int)
    shows = Show.query.paginate(
        page=page, per_page=5, error_out=False)
    next_url = url_for('main.index', page=shows.next_num) \
        if shows.has_next else None
    prev_url = url_for('main.index', page=shows.prev_num) \
        if shows.has_prev else None
    return render_template('index.html', title='Home', 
                           shows=shows.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/show/<show_id>', methods=['GET','POST'])
@login_required
def show_detail(show_id):
    
    show = Show.query.filter_by(id=show_id).first()
    form = BookingForm()
    if form.validate_on_submit():
        
        booking = Booking(date=form.date.data, show_id=form.show_id.data,
                      sheats=form.sheats.data,price=form.price.data,showTime=form.showTime.data,
                      user_id=current_user.id)
        db.session.add(booking)
        db.session.commit()
        flash('Your booking have been confirmed.')
        return redirect(url_for('main.index'))
    
    return render_template('show_detail.html', title=show.name,
                           show=show, form=form)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    bookings = user.bookings.order_by(Booking.timestamp.desc()).paginate(
        page=page, per_page=5,
        error_out=False)
    next_url = url_for('main.user', username=user.username,
                       page=bookings.next_num) if bookings.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=bookings.prev_num) if bookings.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, bookings=bookings,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/show/<show_id>/<showtime>')
@login_required
def show_booking_status(show_id,showtime):
    show = Show.query.filter_by(id=show_id).first()
    bsheats = Booking.query.with_entities(Booking.sheats).filter_by(show_id=show_id, showTime=showtime).all()
    booked_sheat = list()
    for bsheat in bsheats:
        for i in bsheat:
            booked_sheat.append(i)
        
    booked_sheat = [int(item) for items in booked_sheat for item in items.split(",")]
    
    return render_template('seat_popup.html', bookings=booked_sheat,show=show)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/book', methods=['POST'])
@login_required
def book():
    form = BookingForm()
    if form.validate_on_submit():
        
        booking = Booking(date=form.date.data, show_id=form.show_id.data,
                      sheats=form.seats.data,price=form.price.data,ShowTime=form.showTime.data,
                      user_id=current_user.id)
        db.session.commit()
        flash('Your booking have been confirmed.')
        return redirect(url_for('main.index'))
    else:
        return redirect(request.referrer)
    
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/review/<show_id>', methods=['GET','POST'])
@login_required
def review(show_id):
    form = ReviewForm()
    if form.validate_on_submit():
        
        review = Rating(body=form.body.data, ratings=form.ratings.data,show_id=show_id,
                      user_id=current_user.id)
        db.session.add(review)
        db.session.commit()
        flash('Your Rating submited.')
        return redirect(url_for('main.index'))
    
    return render_template("review_form.html", formName="Add review", form=form)



@bp.route('/admin/dashboard', methods=["GET"])
@login_required
@requires_admin
def admin_dashboard():
    
    
    return render_template("admin/dashboard.html")

@bp.route('/admin/venue', methods=["GET"])
@login_required
@requires_admin
def admin_venue():
    venues = Venue.query.all()
    if venues:
        return render_template("admin/venue.html", title="Venues", venues=venues)
    
    
    return render_template("admin/venue.html", title="Venues")


@bp.route('/admin/venue/add', methods=["GET", "POST"])
@login_required
@requires_admin
def admin_venue_add():
    
    form = VenueForm()
    if form.validate_on_submit():
        venue = Venue(name=form.name.data, place=form.place.data,
                      capacity=form.capacity.data)
        db.session.add(venue)
        db.session.commit()
        flash('The venue is stored.')
        return redirect(url_for('main.admin_venue'))
    
    
    return render_template("admin/form.html", formName="Add Venue", form=form)


@bp.route('/admin/show', methods=["GET"])
@login_required
@requires_admin
def admin_show():
    venues = Venue.query.all()
    if venues:
        return render_template("admin/show.html", title="Shows", venues=venues)
    
    flash("No Venue")
    return render_template("admin/show.html")


@bp.route('/admin/shows/<venue_id>', methods=["GET"])
@login_required
@requires_admin
def admin_shows(venue_id):
    shows = Show.query.filter_by(venue_id=venue_id).all()
    if shows:
        return render_template("admin/show_list.html", title="Shows", shows=shows,venue_id=venue_id)
    
    
    return render_template("admin/show_list.html", title="Shows", venue_id=venue_id)


@bp.route('/admin/show/<venue_id>/add', methods=["GET","POST"])
@login_required
@requires_admin
def admin_show_add(venue_id):
    form = ShowForm()
    if form.validate_on_submit():
        show = Show(name=form.name.data, price=int(form.price.data * 10), date_from=form.date_from.data,
                      date_to=form.date_to.data,timing=form.showTime.data,venue_id=venue_id,tags="this")
        db.session.add(show)
        db.session.commit()
        flash('The Show is stored.')
        return redirect(url_for('main.admin_venue'))
    
    
    return render_template("admin/show_form.html", formName="Add Show", form=form)


@bp.route('/admin/addimages/<show_id>', methods=["GET","POST"])
@login_required
@requires_admin
def admin_show_images(show_id):
    form = ImageUploadForm()
    show = Show.query.filter_by(id=show_id).first()
    if form.validate_on_submit():
        
        assets_dir = app.config.UPLOADED_FILES
        img = form.image.data

        filename = secure_filename(img.filename)
        extension = os.path.splitext(img.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        path = img.save(os.path.join(assets_dir, 'image', f_name))
        print(path)
        image = Images(caption=form.caption.data, path=f_name, show_id = show_id)
        db.session.add(image)
        db.session.commit()
        flash('The Show Images are stored.')
        return redirect(url_for('main.admin_show_images', show_id=show_id))
    return render_template("admin/add_image.html", formName="Manage Image", form=form, show=show)


@bp.route('/admin/booking', methods=["GET"])
@login_required
@requires_admin
def admin_booking():
    venues = Venue.query.all()
    if venues:
        return render_template("admin/booking.html", title="Bookings", venues=venues)
    
    flash("No Venue")
    return render_template("admin/booking.html")
