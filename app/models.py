from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import String, Integer, Column
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Employee(db.Model, UserMixin):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    employee_number = Column(Integer, unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
