from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database import Base

class Todo(Base):
    # Define the table name
    __tablename__ = "todos"

    # Define the columns
    id = Column(Integer, primary_key=True, index=True)  # Unique identifier for the todo
    title = Column(String)  # Title of the todo
    complete = Column(Boolean, default=False)  # Flag indicating if the todo is complete or not
