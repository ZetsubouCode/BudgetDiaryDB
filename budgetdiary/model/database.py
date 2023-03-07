from sqlalchemy import Column, DECIMAL, Date, DateTime, ForeignKey, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class IncomeCategory(Base):
    __tablename__ = 'income_category'

    id = Column(INTEGER(11), primary_key=True,autoincrement=True)
    name = Column(String(200), nullable=False)
    emoticon = Column(String(200))


class OutcomeCategory(Base):
    __tablename__ = 'outcome_category'

    id = Column(INTEGER(11), primary_key=True,autoincrement=True)
    name = Column(String(200), nullable=False)
    emoticon = Column(String(200))


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER(11), primary_key=True,autoincrement=True)
    discord_username = Column(String(200), nullable=False, unique=True)
    pin = Column(String(45))
    balance = Column(DECIMAL(12, 2), nullable=False, server_default=text("0.00"))
    date_created = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

class Income(Base):
    __tablename__ = 'income'

    id = Column(INTEGER(11), primary_key=True, nullable=False,autoincrement=True)
    income_category_id = Column(ForeignKey('income_category.id'), primary_key=True, nullable=False, index=True)
    user_id = Column(ForeignKey('user.id'), primary_key=True, nullable=False, index=True)
    description = Column(String(250), nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False, server_default=text("0.00"))
    date_created = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    income_category = relationship('IncomeCategory')
    user = relationship('User')


class MonthlySummary(Base):
    __tablename__ = 'monthly_summary'

    id = Column(INTEGER(11), primary_key=True, nullable=False,autoincrement=True)
    user_id = Column(ForeignKey('user.id'), primary_key=True, nullable=False, index=True)
    month = Column(INTEGER(11), nullable=False)
    total_income = Column(DECIMAL(12, 2), nullable=False, server_default=text("0.00"))
    total_outcome = Column(DECIMAL(12, 2), nullable=False, server_default=text("0.00"))
    date_created = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    user = relationship('User')


class Outcome(Base):
    __tablename__ = 'outcome'

    id = Column(INTEGER(11), primary_key=True, nullable=False,autoincrement=True)
    outcome_category_id = Column(ForeignKey('outcome_category.id'), primary_key=True, nullable=False, index=True)
    user_id = Column(ForeignKey('user.id'), primary_key=True, nullable=False, index=True)
    description = Column(String(250), nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False, server_default=text("0.00"))
    date_created = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    outcome_category = relationship('OutcomeCategory')
    user = relationship('User')
    
class OutcomePlan(Base):
    __tablename__ = 'outcome'

    id = Column(INTEGER(11), primary_key=True, nullable=False,autoincrement=True)
    outcome_category_id = Column(ForeignKey('outcome_category.id'), primary_key=True, nullable=False, index=True)
    user_id = Column(ForeignKey('user.id'), primary_key=True, nullable=False, index=True)
    description = Column(String(250), nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False, server_default=text("0.00"))
    date_spend = Column(Date, nullable=False)
    date_created = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    outcome_category = relationship('OutcomeCategory')
    user = relationship('User')


class Saving(Base):
    __tablename__ = 'saving'

    id = Column(INTEGER(11), primary_key=True, nullable=False,autoincrement=True)
    user_id = Column(ForeignKey('user.id'), primary_key=True, nullable=False, index=True)
    description = Column(String(200), nullable=False)
    date_created = Column(DateTime, nullable=False,server_default=text("current_timestamp()"))
    amount = Column(DECIMAL(12, 2), nullable=False)
    due_date = Column(Date, nullable=False)

    user = relationship('User')
