from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import (
      Table,
      Order,
      OrderDetail,
      Employee,
      Menu,
      MenuItem,
      MenuItemType
)
from app.forms import HostForm, AddToOrder
bp = Blueprint('orders', __name__, url_prefix="")


@bp.route("/")
@login_required
def main():
    # Query and filter for open tables
    table_list = Table.query.order_by(Table.number).all()
    open_tables = [(table.id, f"Table {table.number}")
                   for table in table_list
                   if table.id not in [order.id for order in
                   Order.query.filter(Order.closed != False)]]  # noqa
    # Query all employees to assign tables
    employees = Employee.query.order_by(Employee.name).all()
    servers = [(employee.id, f"{employee.name}") for employee in employees]
    form = HostForm(tables=0)
    form.tables.choices = open_tables
    form.tables.choices.insert(0, (0, "Select a Table"))
    form.servers.choices = servers
    form.servers.choices.insert(0, (0, 'Select a Server'))

    orders = Order.query \
        .filter(Order.employee_id == current_user.id) \
        .filter(Order.closed == False)  # noqa

    menu_items = MenuItem.query \
        .join(MenuItemType) \
        .order_by(MenuItemType.name, MenuItem.name) \
        .options(db.joinedload(MenuItem.type))

    menu = {}
    for i in menu_items:
        menu[i.type.name] = []
        menu[i.type.name].append(i)

    return render_template('orders.html',
                           form=form,
                           orders=orders,
                           menu=menu)


@bp.route('/orders/<int:id>/add', methods=['POST'])
@login_required
def add_to_order(id):
    form = AddToOrder()
    # Get the selected items from the food-list form
    form.menu_item_ids.choices = [(item.id, '')
                                  for item in MenuItem.query.all()]
    if form.validate_on_submit():
        order = Order.query.get(id)
        for menu_item_id in form.menu_item_ids.data:
            db.session.add(OrderDetail(order=order, menu_item_id=menu_item_id))
        db.session.commit()
    return redirect(url_for('.main'))


@bp.route('/orders/<int:id>')
@login_required
def show_details(id):
    pass


@bp.route('tables/assign', methods=['POST'])
@login_required
def assign_table():
    


@bp.route('/orders/<int:id>/close', methods=['POST'])
@login_required
def close_order(id):
    order = Order.query.get(id)
    order.closed = True
    db.session.commit()
    return redirect(url_for('.main'))
