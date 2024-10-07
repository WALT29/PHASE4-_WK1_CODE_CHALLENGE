from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # add relationship
    heropowers=db.relationship('HeroPower',back_populates='heroes' ,cascade='all,delete-orphan')
    powers=association_proxy('heropowers','power',creator=lambda power_obj:HeroPower(power=power_obj))
    # add serialization rules
    serialize_rules=('-heropowers.hero',)

    def __repr__(self):
        return f'<Hero {self.id}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String,nullable=False)

    # add relationship
    heropowers=db.relationship('HeroPower',back_populates='power',cascade='all,delete-orphan')
    heroes=association_proxy('heropowers','hero',creator=lambda hero_obj:HeroPower(hero=hero_obj))
    

    # add serialization rules
    serialize_rules=('-heropowers.power',)

    # add validation
    @validates('description')
    def validates_description(self,key,description):
        if len(description) < 20:
            raise ValueError('The description must be at least 20 characters')
        return description

    def __repr__(self):
        return f'<Power {self.id}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # add relationships
    hero_id=db.Column(db.Integer,db.ForeignKey('heroes.id'))
    power_id=db.Column(db.Integer,db.ForeignKey('powers.id'))
    
    hero=db.relationship('Hero',back_populates='heropowers')
    power=db.relationship('Power',back_populates='heropowers')
    
    # add serialization rules
    serialize_rules=('-power.heropowers','hero.heropowers',)
    

    # add validation
    @validates('strength')
    def validates_strength(self,key,strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError('Entered strength must be either Strong, Weak, Average')
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}>'
