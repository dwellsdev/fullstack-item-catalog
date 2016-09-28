from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

def create_restaurant(name):
    session = DBSession()

    new_restaurant = Restaurant(name=name)

    session.add(new_restaurant)
    session.commit()


def create_menu_item(name, description, price, course, restaurant):
    session = DBSession()

    print(restaurant)

    restaurant_obj = session.query(Restaurant).filter_by(name = restaurant).one()

    new_menu_item = MenuItem(name=name, description=description, price=price,
                            course=course, restaurant=restaurant_obj)

    session.add(new_menu_item)
    session.commit()

def update_restaurant(restaurant, new_name):
    session = DBSession()

    update_restaurant = session.query(Restaurant).filter_by(name = restaurant).one()

    update_restaurant.name = new_name

    session.add(update_restaurant)
    session.commit()

def update_menu_item(original_restaurant, menu_item, name="", description="",
                    price="", course="", restaurant=""):

    session = DBSession()

    update_item = session.query(MenuItem).filter_by(name = menu_item).one()

    if name:
        update_item.name = name

    if description:
        update_item.description = description

    if price:
        update_item.price = price

    if course:
        update_item.course = course

    if restaurant:
        update_item.restaurant = restaurant

    session.add(update_item)
    session.commit()
