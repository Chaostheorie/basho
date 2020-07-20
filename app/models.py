import typing
from secrets import token_urlsafe
from hashlib import md5
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, app


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(90), unique=True)

    @db.bake
    def get_by_name_query(self):
        return self.query.where(self.name == db.bindparam("name"))

    @staticmethod
    async def get_by_name(name: str):
        return await Role.get_by_name_query.first(name=name)

    def __repr__(self) -> str:
        return f"<Role {self.name} [{self.id}]>"


class UserRoles(db.Model):
    __tablename__ = "userroles"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="CASCADE"))

    def __repr__(self) -> str:
        return f"<UserRole p:{self.user_id}/g:{self.role_id}>"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(90), unique=True)
    e_mail = db.Column(db.String(128), unique=True)
    gravatar = db.Column(db.Boolean, server_default="0")
    password = db.Column(db.String(158))
    meta = db.Column(db.JSON)
    token = db.Column(db.String(342), unique=True)
    token_expiration = db.Column(db.DateTime)
    is_superuser = db.Column(db.Boolean, nullable=False, server_default="0")
    is_suspended = db.Column(db.Boolean, nullable=False, server_default="0")

    @property
    def is_authenticated(self) -> bool:
        return self.is_suspended is True

    def avatar(self, size: int) -> str:
        digest = md5(self.username.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size
        )

    async def get_roles(self):
        """Gets roles of user with baked query"""
        return await self.get_role_query.all(uid=self.id)

    @staticmethod
    async def get_by_username(username: str):
        """Gets User by username with baked query"""
        return await User.get_by_username_query.first(username=username)

    @db.bake
    def get_role_query(self):
        """Constructs Query for getting Roles of User for baking"""
        query = Role.outerjoin(UserRoles).outerjoin(self)
        query = query.select().where(UserRoles.user_id == db.bindparam("uid"))
        loader = Role.distinct(Role.id).load(add_parent=self.distinct(self.id))
        return query.execution_options(loader=loader)

    @db.bake
    def get_by_username_query(self):
        """Constructs Query for getting Users by username"""
        query = self.query.where(self.username == db.bindparam("username"))
        return query

    @staticmethod
    def gen_password(password: str) -> str:
        if len(password) == 128:
            raise ValueError("Password length collides with token")
        return generate_password_hash(password, method="pbkdf2:sha512")

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def generate_token(self) -> str:
        """Generates authentication usable token

        Returns:
            str: token (342 chars long, 64 bytes)
        """
        token = token_urlsafe(64)
        self.token = generate_password_hash(token)
        return token

    def verify_by_token(self, token: str) -> bool:
        return check_password_hash(self.token, token)

    def jsonify(self) -> dict:
        return dict(id=self.id, username=self.username, e_mail=self.e_mail)

    def add_role(self, role: Role) -> None:
        self._roles.add(role)
        role._users.add(self)

    @property
    def roles(self) -> list:
        return self._roles

    def __repr__(self) -> str:
        return f"<User {self.username} [{self.id}]>"


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    nick = db.Column(db.String(90), unique=True)
    description = db.Column(db.Text())
    meta = db.Column(db.JSON)

    master_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))

    @db.bake
    def get_by_nick_query(self):
        return self.query.where(self.nick == db.bindparam("nick"))

    @staticmethod
    async def get_by_nick(nick: str):
        return await Room.get_by_nick_query.first(nick=nick)

    @db.bake
    def overview_paginated_query(self):
        query = (
            self.query.offset(db.bindparam("offset"))
            .limit(db.bindparam("limit"))
            .order_by(self.nick.desc())
        )
        return query

    @staticmethod
    async def overview_paginated(offset: int, limit: int) -> list:
        return await Room.overview_paginated_query.all(offset=offset, limit=limit)

    def get_links(self) -> list:
        return [(f"/room/view/{self.id}", "Ansehen")]

    def __repr__(self) -> str:
        return f"<Room {self.id} [{self.nick}]>"


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    is_public = db.Column(db.Boolean)
    meta = db.Column(db.JSON)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)

    @db.bake
    def overview_paginated_query(self):
        query = self.query.where(self.is_public == True)
        query.offset(db.bindparam("offset")).limit(db.bindparam("limit"))
        query.order_by(self.start.desc())
        return query

    @staticmethod
    async def overview_paginated(offset: int, limit: int) -> list:
        """Gets paginated slices o public reservations for EventsOverviewRoute

        Args:
            offset (int): Query Offset
            limit (int): Query Limit

        Returns:
            list: List of Reservations maybe List of Reservations or empty list
        """
        return await Reservation.overview_paginated_query.all(
            offset=offset, limit=limit
        )
