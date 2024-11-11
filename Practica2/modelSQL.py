from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Numeric, Boolean, func, Text, SmallInteger, Date
from sqlalchemy import Date
import sqlalchemy as sql

username = 'alumnodb'
password = '1234'
host = 'localhost'
port = '5432'
database = 'si1'

DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/{database}'

engine = sql.create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    
    orderid = Column(Integer, primary_key=True, autoincrement=True)
    orderdate = Column(Date, nullable=False)
    customerid = Column(Integer, ForeignKey('customers.customerid'), nullable=True)
    netamount = Column(Numeric, nullable=True)
    tax = Column(Numeric, nullable=True)
    totalamount = Column(Numeric, nullable=True)
    status = Column(String(10), nullable=True)

    customer = relationship("Customer", back_populates="orders")

    orderdetails = relationship("OrderDetail", back_populates="order")

class Customer(Base):
    __tablename__ = 'customers'

    customerid = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(50), nullable=False)
    email = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False)
    password = Column(String(128), nullable=False)
    balance = Column(Numeric(10, 2), nullable=True, default = 0.00)

    orders = relationship("Order", back_populates="customer")
    ratings = relationship("Rating", back_populates="customer")
    creditcards = relationship("CreditcardCustomer", back_populates="customer")

class Rating(Base):
    __tablename__ = 'ratings'

    customerid = Column(Integer, ForeignKey('customers.customerid'), primary_key=True, nullable=False)
    movieid = Column(Integer, ForeignKey('imdb_movies.movieid'), primary_key=True, nullable=False)
    likes = Column(Boolean, nullable=True)
    rating_date = Column(Date, nullable=True, default=func.current_timestamp())

    customer = relationship("Customer", back_populates="ratings")
    movie = relationship("ImdbMovie", back_populates="ratings")

class OrderDetail(Base):
    __tablename__ = 'orderdetail'

    orderid = Column(Integer, ForeignKey('orders.orderid'), primary_key=True, nullable=False)
    prod_id = Column(Integer, ForeignKey('products.prod_id'), primary_key=True, nullable=False)
    price = Column(Numeric, nullable=True)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="orderdetails")
    product = relationship("Product", back_populates="orderdetails")

class ImdbDirectorMovies(Base):
    __tablename__ = 'imdb_director_movies'

    directorid = Column(Integer, ForeignKey('imdb_directors.directorid'), primary_key=True, nullable=False)
    movieid = Column(Integer, ForeignKey('imdb_movies.movieid'), primary_key=True, nullable=False)
    numparticipation = Column(Integer, primary_key=True, nullable=False)
    ascharacter = Column(Text, nullable=True)
    participation = Column(Text, nullable=True)
    isarchivefootage = Column(SmallInteger, nullable=False, default=0)
    isuncredited = Column(SmallInteger, nullable=False, default=0)
    iscodirector = Column(SmallInteger, nullable=False, default=0)
    ispilot = Column(SmallInteger, nullable=False, default=0)
    ischief = Column(SmallInteger, nullable=False, default=0)
    ishead = Column(SmallInteger, nullable=False, default=0)

    director = relationship("ImdbDirector", back_populates="movies")
    movie = relationship("ImdbMovie", back_populates="directors")

class ImdbDirector(Base):
    __tablename__ = 'imdb_directors'

    directorid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    directorname = Column(String(128), nullable=False)

    movies = relationship("ImdbDirectorMovies", back_populates="director")

class ImdbActor(Base):
    __tablename__ = 'imdb_actors'

    actorid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    actorname = Column(String(128), nullable=False)
    gender = Column(String(6), nullable=False)

    movies = relationship("ImdbActorMovies", back_populates="actor")

class ImdbActorMovies(Base):
    __tablename__ = 'imdb_actor_movies'

    actorid = Column(Integer, ForeignKey('imdb_actors.actorid'), primary_key=True, nullable=False)
    movieid = Column(Integer, ForeignKey('imdb_movies.movieid'), primary_key=True, nullable=False)
    character = Column(String, nullable=True)
    ascharacter = Column(Text, nullable=True)
    isvoice = Column(SmallInteger, nullable=False, default=0)
    isarchivefootage = Column(SmallInteger, nullable=False, default=0)
    isuncredited = Column(SmallInteger, nullable=False, default=0)
    creditdisposition = Column(Integer, nullable=False, default=0)

    actor = relationship("ImdbActor", back_populates="movies")
    movie = relationship("ImdbMovie", back_populates="actors")

class ImdbMovie(Base):
    __tablename__ = 'imdb_movies'

    movieid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    movietitle = Column(String(255), nullable=False)
    movierelease = Column(String(192), nullable=False)
    movietype = Column(Integer, nullable=False)
    year = Column(Text, nullable=True)
    issuspended = Column(SmallInteger, nullable=False, default=0)

    actors = relationship("ImdbActorMovies", back_populates="movie")
    directors = relationship("ImdbDirectorMovies", back_populates="movie")
    countries = relationship("ImdbMovieCountries", back_populates="movie")
    genres = relationship("ImdbMovieGenres", back_populates="movie")
    languages = relationship("ImbdMovieLanguages", back_populates="movie")
    ratings = relationship("Rating", back_populates="movie")
    products = relationship("Product", back_populates="movie")

class Product(Base):
    __tablename__ = 'products'

    prod_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    movieid = Column(Integer, ForeignKey('imdb_movies.movieid'), nullable=False)
    price = Column(Numeric, nullable=False)
    description = Column(String(30), nullable=False)

    movie = relationship("ImdbMovie", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    orderdetails = relationship("OrderDetail", back_populates="product")

class Inventory(Base):
    __tablename__ = 'inventory'

    prod_id = Column(Integer, ForeignKey('products.prod_id'), primary_key=True, nullable=False)
    stock = Column(Integer, nullable=False)
    sales = Column(Integer, nullable=False)

    product = relationship("Product", back_populates="inventory")

class ImdbMovieCountries(Base):
    __tablename__ = 'imdb_moviecountries'

    movieid = Column(Integer, ForeignKey('imdb_movies.movieid'), primary_key=True, nullable=False)
    country = Column(String(32), primary_key=True, nullable=False)

    movie = relationship("ImdbMovie", back_populates="countries")
    
class ImdbMovieGenres(Base):
    __tablename__ = 'imdb_moviegenres'

    movieid = Column(Integer, ForeignKey('imdb_movies.movieid'), primary_key=True, nullable=False)
    genre = Column(String(32), primary_key=True, nullable=False)

    movie = relationship("ImdbMovie", back_populates="genres")

class ImbdMovieLanguages(Base):
    __tablename__ = 'imdb_movielanguages'

    movieid = Column(Integer, ForeignKey('imdb_movies.movieid'), primary_key=True, nullable=False)
    language = Column(String(32), primary_key=True, nullable=False)
    extrainformation = Column(String(128), primary_key=True, nullable=True)

    movie = relationship("ImdbMovie", back_populates="languages")

class CreditcardCustomer(Base):
    __tablename__ = 'creditcardcustomer'

    customerid = Column(Integer, ForeignKey('customers.customerid'), primary_key=True, nullable=False)
    creditcard = Column(String(50), primary_key=True, nullable=False)
    exp_date = Column(Date, nullable=False)
    cvv = Column(String(3), nullable=False)
    cardholder = Column(String(128), nullable=False)

    customer = relationship("Customer", back_populates="creditcards")