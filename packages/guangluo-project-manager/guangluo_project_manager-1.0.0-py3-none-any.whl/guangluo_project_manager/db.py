from datetime import datetime
from pony.orm import *

db = Database()


class Projects(db.Entity):
    """项目"""
    _table_ = 'projects'
    id = PrimaryKey(int, auto=True)
    name = Required(str, 255, unique=True)
    archived = Required(bool, default=False)
    create_time = Optional(datetime, precision=0, default=lambda: datetime.now())
    update_time = Optional(datetime, precision=0, default=lambda: datetime.now())
