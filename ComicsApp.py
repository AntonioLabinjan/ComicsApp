from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "Blabla blabla"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:AN1246A301JA@localhost/ComicsApp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Comic(db.Model):
    comic_identificator = db.Column(db.Integer, primary_key = True)
    comic_name = db.Column(db.String(100))
    comic_number = db.Column(db.Integer)
    comic_hero = db.Column(db.String(100))
    comic_pageNum = db.Column(db.Integer)
    comic_publisher = db.Column(db.String(100))
    
    def __init__(self, comic_identificator, comic_name, comic_number, comic_hero, comic_pageNum, comic_publisher):
    
        self.comic_identificator = comic_identificator
        self.comic_name = comic_name
        self.comic_number = comic_number
        self.comic_hero = comic_hero
        self.comic_pageNum = comic_pageNum
        self.comic_publisher = comic_publisher
    

@app.route('/')
def Index():
    hero_name = request.args.get('hero_name')
    
    if hero_name:
        all_comics = Comic.query.filter_by(comic_hero=hero_name).all()
    else:
        all_comics = Comic.query.all()
    
    return render_template("index.html", comics=all_comics)
        
        
@app.route('/insert_comic', methods = ['POST'])
def insert_comic():

    if request.method == 'POST':
    
        comic_identificator = request.form['comic_identificator']
        comic_name = request.form['comic_name']
        comic_number = request.form['comic_number']
        comic_hero = request.form['comic_hero']
        comic_pageNum = request.form['comic_pageNum']
        comic_publisher = request.form['comic_publisher']
        
        my_comic = Comic(comic_identificator, comic_name, comic_number, comic_hero, comic_pageNum, comic_publisher)
        db.session.add(my_comic)
        db.session.commit()
        
        flash("COMIC HAS BEEN INSERTED SUCCESSFULLY AT: "+ datetime.now().strftime("%H:%M"))
        
        return redirect(url_for('Index'))
        
@app.route('/update_comic', methods = ['GET', 'POST'])
def update_comic():
    
    if request.method == 'POST':
        my_comic = Comic.query.get(request.form.get('comic_identificator'))
        
        my_comic.comic_name = request.form['comic_name']
        my_comic.comic_number = request.form['comic_number']
        my_comic.comic_hero = request.form['comic_hero']
        my_comic.comic_pageNum = request.form['comic_pageNum']
        my_comic.comic_publisher = request.form['comic_publisher']
        
        db.session.commit()
        flash("COMIC HAS BEEN UPDATED SUCCESSFULLY AT: "+datetime.now().strftime("%H:%M"))
        
        return redirect(url_for('Index'))
        
@app.route('/delete_comic/<comic_identificator>/', methods = ['GET', 'POST'])
def delete_comic(comic_identificator):
    my_comic = Comic.query.get(comic_identificator)
    db.session.delete(my_comic)
    db.session.commit()
    flash("COMIC HAS BEEN DELETED SUCCESSFULLY AT: "+datetime.now().strftime("%H:%M"))
    
    return redirect(url_for('Index'))
    
@app.route('/calculate_total_pages')
def calculate_total_pages():
    total_pages = 0  

    all_comics = Comic.query.all() 

    for comic in all_comics:
        total_pages += comic.comic_pageNum 

    flash("Total pages: " + str(total_pages)) 

    return redirect(url_for('Index'))


@app.route('/filter_comics', methods=['POST'])
def filter_comics():
    hero_name = request.form['hero_name']
    
    filtered_comics = Comic.query.filter_by(comic_hero=hero_name).all()
    
    if not filtered_comics:
        flash("You don't have this hero in your collection")
    
    return render_template("index.html", comics=filtered_comics)

@app.route('/search_comics', methods=['POST'])
def search_comics():
    comic_name = request.form.get('comic_name')
    filtered_comics = Comic.query.filter(Comic.comic_name.ilike(f'%{comic_name}%')).all()

    if not filtered_comics:
        flash("No comics found with that name.")
        return redirect(url_for('Index'))

    return render_template("index.html", comics=filtered_comics)


import random

@app.route('/random_comic')
def random_comic():
    all_comics = Comic.query.all()
    
    if not all_comics:
        flash("Your collection is empty.")
        return redirect(url_for('Index'))
    
    random_comic = random.choice(all_comics)
    
    return render_template("index.html", comics=[random_comic])

if (__name__ == "__main__"):
    app.run(debug=True)
    
    
    
    
    