from datetime import datetime
from sqlalchemy import ARRAY, Column, Integer, String
from init import db
from sqlalchemy.ext.hybrid import hybrid_property

# many-to-many relationship between typealists and typeblists
typealist_tybeblist = db.Table("typealist_tybeblist",
                          db.Column(
                            "typealist_id",
                            db.Integer,
                            db.ForeignKey("TypeAList.id"),
                            primary_key=True
                          ),
                          db.Column(
                            "typeblist_id",
                            db.Integer,
                            db.ForeignKey("TypeBList.id"),
                            primary_key=True
                          )
                          )


class TypeAList(db.Model):
    __tablename__ = 'TypeAList'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    options = db.Column(ARRAY(String), nullable=False)
    # implementing a many-to-one relationship (from the `TypeAList` perspective) with `Item` entity
    items = db.relationship(
        "Item",
        backref="typealist",
        lazy=True,
        collection_class=list,
        cascade="all, delete-orphan"
    )
    # implementing a many-to-many relationship with `TypeBList` entity
    typeblists = db.relationship(
        "TypeBList",
        secondary=typealist_tybeblist,
        backref=db.backref("typealists", lazy=True)
    )

    # using hybrid properties here to handle getting data from base fields
    _upcoming_items = Column("upcoming_items", Integer)
    @hybrid_property
    def upcoming_items(self):
        return db.session.query(Item).join(TypeAList).filter(
            Item.typealist_id == self.id
        ).filter(Item.start_time > datetime.now()).all()

    _past_items = Column("past_items", Integer)
    @hybrid_property
    def past_items(self):
        return db.session.query(Item).join(TypeAList).filter(
            Item.typealist_id == self.id
        ).filter(Item.start_time < datetime.now()).all()

    _past_items_count = Column("past_items_count", Integer)
    @hybrid_property
    def past_items_count(self):
        return db.session.query(Item).join(TypeAList).filter(
            Item.typealist_id == self.id
        ).filter(Item.start_time < datetime.now()).count()

    _upcoming_items_count = Column("upcoming_items_count", Integer)
    @hybrid_property
    def upcoming_items_count(self):
        return db.session.query(Item).join(TypeAList).filter(
            Item.typealist_id == self.id
        ).filter(Item.start_time > datetime.now()).count()


class TypeBList(db.Model):
    __tablename__ = 'TypeBList'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    items = db.relationship(
        "Item",
        backref="typeblist",
        lazy=True,
        collection_class=list,
        cascade="all, delete-orphan"
    )

    _upcoming_items = Column("upcoming_items", Integer)
    @hybrid_property
    def upcoming_items(self):
        return db.session.query(Item).join(TypeBList).filter(
            Item.typeblist_id == self.id
        ).filter(Item.start_time > datetime.now()).all()

    _past_items = Column("past_items", Integer)
    @hybrid_property
    def past_items(self):
        return db.session.query(Item).join(TypeBList).filter(
            Item.typeblist_id == self.id
        ).filter(Item.start_time < datetime.now()).all()

    _past_items_count = Column("past_items_count", Integer)
    @hybrid_property
    def past_items_count(self):
        return db.session.query(Item).join(TypeBList).filter(
            Item.typeblist_id == self.id
        ).filter(Item.start_time < datetime.now()).count()

    _upcoming_items_count = Column("upcoming_items_count", Integer)
    @hybrid_property
    def upcoming_items_count(self):
        return db.session.query(Item).join(TypeBList).filter(
            Item.typeblist_id == self.id
        ).filter(Item.start_time > datetime.now()).count()


class Item(db.Model):
    __tablename__ = 'Item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # this entity has 2 one-to-many relationships with both types of lists
    typealist_id = db.Column(
        db.Integer,
        db.ForeignKey("TypeAList.id"),
        nullable=False
    )
    typeblist_id = db.Column(db.Integer, db.ForeignKey("TypeBList.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # hybrid props
    _typealist_name = Column("typealist_name", String())
    @hybrid_property
    def typealist_name(self):
        return self.typealist.name

    _typeblist_name = Column("typeblist_name", String())
    @hybrid_property
    def typeblist_name(self):
        return self.typeblist.name
