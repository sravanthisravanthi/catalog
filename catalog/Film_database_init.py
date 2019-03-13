from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from Film_setup import *

engine = create_engine('sqlite:///films.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
session = DBSession()

# Delete FilmCategoryName if exisitng.
session.query(FilmCategoryName).delete()
# Delete FilmName if exisitng.
session.query(FilmName).delete()
# Delete User if exisitng.
session.query(User).delete()

# Create sample users data
User1 = User(name="Sravanthi Munnaluri", email="sravanthimunnaluri@gmail.com")
session.add(User1)
session.commit()
print ("Successfully Add First User")
# Create sample film categories
Category1 = FilmCategoryName(name="DRAMA", user_id=1)
session.add(Category1)
session.commit

Category2 = FilmCategoryName(name="ROMANCE", user_id=1)
session.add(Category2)
session.commit()

Category3 = FilmCategoryName(name="SCIENCE FICTION", user_id=1)
session.add(Category3)
session.commit()

Category4 = FilmCategoryName(name="THRILLER", user_id=1)
session.add(Category4)
session.commit()

Category5 = FilmCategoryName(name="POLITICAL", user_id=1)
session.add(Category5)
session.commit()

# Populare films

Name5 = FilmName(
    moviename="Bahubali 2-The Conclusion",
    year="2017",
    rating="Awesome",
    action="2D",
    budget="250 Cr",
    date=datetime.datetime.now(),
    filmcategorynameid=1,
    user_id=1)
session.add(Name5)
session.commit()

Name6 = FilmName(
    moviename="F2-Fun and Frustration",
    year="2019",
    rating="Average",
    action="2D",
    budget="45 cr",
    date=datetime.datetime.now(),
    filmcategorynameid=1,
    user_id=1)
session.add(Name6)
session.commit()

Name7 = FilmName(
    moviename="N.T.R Kathanayakudu",
    year="2019",
    rating="Average",
    action="2D",
    budget="65 cr",
    date=datetime.datetime.now(),
    filmcategorynameid=1,
    user_id=1)
session.add(Name7)
session.commit()

Name8 = FilmName(
    moviename="Arjun Reddy",
    year="2017",
    rating="Average",
    action="2D",
    budget="51 cr",
    date=datetime.datetime.now(),
    filmcategorynameid=1,
    user_id=1)
session.add(Name8)
session.commit()

Name9 = FilmName(
    moviename="Vinaya vidheya Rama",
    year="2019",
    rating="Average",
    action="2D",
    budget="65",
    date=datetime.datetime.now(),
    filmcategorynameid=1,
    user_id=1)
session.add(Name9)
session.commit()


Name10 = FilmName(
    moviename="Fidaa",
    year="2017",
    rating="Awesome",
    action="2D",
    budget="78 Cr",
    date=datetime.datetime.now(),
    filmcategorynameid=2,
    user_id=1)
session.add(Name10)
session.commit()

Name11 = FilmName(
    moviename="Tulasi",
    year="2007",
    rating="Average",
    action="2D",
    budget="45cr",
    date=datetime.datetime.now(),
    filmcategorynameid=2,
    user_id=1)
session.add(Name11)
session.commit()


Name12 = FilmName(
    moviename="Hello Guru Prema Kosame",
    year="2018",
    rating="Average",
    action="2D",
    budget="55 cr",
    date=datetime.datetime.now(),
    filmcategorynameid=2,
    user_id=1)
session.add(Name12)
session.commit()

Name13 = FilmName(
    moviename="Antariksham",
    year="2018",
    rating="Average",
    action="2D",
    budget="25 cr",
    date=datetime.datetime.now(),
    filmcategorynameid=3,
    user_id=1)
session.add(Name13)
session.commit()

Name14 = FilmName(
    moviename="Robo 2.0",
    year="2018",
    rating="Awesome",
    action="2D",
    budget="543 cr",
    date=datetime.datetime.now(),
    filmcategorynameid=3,
    user_id=1)
session.add(Name14)
session.commit()


Name15 = FilmName(
    moviename="Krrish 3",
    year="2013",
    rating="Average",
    action="2D",
    budget="115cr",
    date=datetime.datetime.now(),
    filmcategorynameid=3,
    user_id=1)
session.add(Name15)
session.commit()

Name16 = FilmName(
    moviename="Saaho",
    year="2019",
    rating="Average",
    action="2D",
    budget="300cr",
    date=datetime.datetime.now(),
    filmcategorynameid=3,
    user_id=1)
session.add(Name16)
session.commit()


Name17 = FilmName(
    moviename="U Turn"
    year="2018",
    rating="Average",
    action="2D",
    budget="45cr",
    date=datetime.datetime.now(),
    filmcategorynameid=4,
    user_id=1)
session.add(Name17)
session.commit()

Name18 = FilmName(
    moviename="Bhaagamathie",
    year="2018",
    rating="Average",
    action="2D",
    budget="69cr",
    date=datetime.datetime.now(),
    filmcategorynameid=4,
    user_id=1)
session.add(Name18)
session.commit()

Name19 = FilmName(
    moviename="PSV Garuda Vega",
    year="2017",
    rating="Awesome",
    action="2D",
    budget="55cr",
    date=datetime.datetime.now(),
    filmcategorynameid=4,
    user_id=1)
session.add(Name19)
session.commit()

Name20 = FilmName(
    moviename="Bharat Ane Nenu",
    year="2018",
    rating="Awesome",
    action="2D",
    budget="225cr",
    date=datetime.datetime.now(),
    filmcategorynameid=5,
    user_id=1)
session.add(Name20)
session.commit()

Name21 = FilmName(
    moviename="Leader",
    year="2010",
    rating="Average",
    action="2D",
    budget="48cr",
    date=datetime.datetime.now(),
    filmcategorynameid=5,
    user_id=1)
session.add(Name21)
session.commit()

Name22 = FilmName(
    moviename="Prasthanam",
    year="2010",
    rating="Excellent",
    action="2D",
    budget="3cr",
    date=datetime.datetime.now(),
    filmcategorynameid=5,
    user_id=1)
session.add(Name22)
session.commit()

Name23 = FilmName(
    moviename="Cameraman Gangatho Rambabu",
    year="2012",
    rating="Average",
    action="2D",
    budget="25cr",
    date=datetime.datetime.now(),
    filmcategorynameid=5,
    user_id=1)
session.add(Name23)
session.commit()


print("Your films database has been inserted!")
