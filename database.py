from dotenv import load_dotenv
load_dotenv()

from app import app, db  # noqa
from app.models import (
      Employee,
      Table,
      Order,
      OrderDetail,
      Menu,
      MenuItem,
      MenuItemType
)  # noqa


with app.app_context():
    db.drop_all()
    db.create_all()

    tables = []
    employee = Employee(
        name="Margot",
        employee_number=1234,
        password="password"
    )

    tables.append(employee)

    beverages = MenuItemType(name='Beverages')
    entrees = MenuItemType(name='Entrees')
    sides = MenuItemType(name='Sides')

    dinner = Menu(name='Dinner')

    fries = MenuItem(name="French fries", price=3.50, type=sides, menu=dinner)
    drp = MenuItem(name="Dr. Pepper", price=1.0, type=beverages, menu=dinner)
    jambalaya = MenuItem(name="Jambalaya", price=21.98, type=entrees, menu=dinner)  # noqa

    tables.append(dinner)

    for i in range(1, 11):
        table = Table(number=i, capacity=4 if i <= 5 else 7)
        db.session.add(table)

    table = Table(number=11, capacity=4)
    order = Order(employee=employee, table=table, closed=False)
    order_detail = OrderDetail(order=order, item=fries)

    db.session.add_all(tables)
    db.session.add(table)
    db.session.add(order)
    db.session.commit()
