import os
import json
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from flask import Flask
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
metadata = MetaData()

# Create tables
site = Table('site', metadata,
  Column('id', Integer, primary_key=True),
  Column('name', String(100))
)

category = Table('category', metadata,
  Column('id', Integer, primary_key=True),
  Column('name', String(100))
)

article = Table('article', metadata,
  Column('id', Integer, primary_key=True),
  Column('summary', String(100)),
  Column('source', String(100)),
  Column('site_id', String(100)),
  Column('category_id', Integer)
)

engine = create_engine(os.environ['DATABASE_URL'])
inspector = inspect(engine)

@app.before_first_request
def initialize_database():
    metadata.create_all(engine)
    with engine.connect() as con:
      con.execute("TRUNCATE category")
      con.execute("TRUNCATE site")
      con.execute("INSERT INTO category (name) VALUES ('Asia'), ('World'), ('Business')")
      con.execute("INSERT INTO site (name) VALUES ('Channel News Asia'), ('The Straight Times'), ('Today Online')")

# Home
@app.route('/')
def index():
  return 'Shortnews API'

# Get sites
@app.route('/site')
def site():
  site_list = []
  with engine.connect() as con:
    for site in con.execute('SELECT name FROM site'):
      site_list.append(site.name)
  
  return json.dumps(site_list)

# Get categories
@app.route('/category')
def category():
  category_list = []
  with engine.connect() as con:
    for category in con.execute('SELECT name FROM category'):
      category_list.append(category.name)
    
  return json.dumps(category_list)

# Get articles
@app.route('/articles')
def articles():
  article_list = []
  with engine.connect() as con:
    for article in con.execute('SELECT summary FROM article'):
      article_list.append(article.summary)
  
  return json.dumps(article_list)