import sqlalchemy.orm.query
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,FloatField
from wtforms.validators import DataRequired
import requests
api_key="954087a4f935b13fdc646ef12bdf5440"


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#DB class model initialization
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)

db.create_all()

# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()


# def __repr__(self):
#     return f'<Book {self.title}>'

class RateMovieForm(FlaskForm):
    rating = FloatField('Your rating out of 10',validators=[DataRequired()])
    review = StringField('Your Review',validators=[DataRequired()])
    submit=SubmitField("Done")

@app.route("/")
def home():
    # all_movies = db.session.query(Movie).all() kap te gjitha movie objects
    all_movies = Movie.query.order_by(Movie.rating).all() #.all() duhet sepse it returns the results represented by this Query as a list.
    for i in range (len(all_movies)):
        index=len(all_movies)-i
        all_movies[i].ranking=index
    db.session.commit()
    return render_template("index.html",movies=all_movies)


@app.route("/edit",methods=["GET","POST"])
def edit():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    selected_movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        selected_movie.rating=form.rating.data
        selected_movie.review=form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html',form=form)

@app.route("/delete",methods=["GET","POST"])
def delete():
    movie_id = request.args.get("id")
    selected_movie = Movie.query.get(movie_id)
    db.session.delete(selected_movie)
    db.session.commit()
    return redirect(url_for('home'))

class AddMovie(FlaskForm):
    title = StringField('Movie Title',validators=[DataRequired()])
    submit=SubmitField("Add Movie")

api_key="954087a4f935b13fdc646ef12bdf5440"
params={
     "api_key" :"954087a4f935b13fdc646ef12bdf5440",
    "query" : ""
         }


@app.route("/add",methods=["GET","POST"])
def add():
    add_movie=AddMovie()
    if add_movie.validate_on_submit():
        title=add_movie.title.data
        params["query"]=title
        data = requests.get("https://api.themoviedb.org/3/search/movie?", params=params).json()  #making the first api call and collecting general data for tha movie
        results = data["results"]
        return render_template("select.html",movies=results)
    return render_template("add.html",add_movie=add_movie)

@app.route("/select",methods=["GET","POST"])
def select():
    movie_id=request.args.get("id")
    id_data_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    data=requests.get(id_data_url).json() #making the second api call and retrieving specific information

    new_movie = Movie(
        title=data["original_title"],
        year=int(data["release_date"].split("-")[0]),
        description= data["overview"],
        rating=data["vote_average"],
        ranking="",
        review="My favourite character was the caller.",
        img_url="https://image.tmdb.org/t/p/w500/" + data["poster_path"] #tmdb website's database url format
    )
    db.session.add(new_movie)
    db.session.commit()
    #duhet te shkojm tek edit me id e new moviet qe futem
    return redirect(url_for('edit',id=new_movie.id))
    #si tek url_for qe vendosnim nje parameter ekstra,dhe ketu e vendosim dhe e bejme fetch brenda funskionit edit

if __name__ == '__main__':
    app.run(debug=True)
