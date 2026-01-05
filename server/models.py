# Imports
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

# Initialize the SQLAlchemy database instance
db = SQLAlchemy(metadata=metadata)

# Hero model that inherits from db.Model and SerialzerMixin
class Hero(db.Model, SerializerMixin):
    __tablename__ = "heroes"

    # Prevent infinite recursion when serializing relationships
    serialize_rules = ("-hero_powers.hero",)

    # Table Columns with the id column as the primary key.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # Relationship to HeroPower join table
    hero_powers = db.relationship(
        "HeroPower",
        back_populates="hero",
        cascade="all, delete-orphan"
    )

# Power model that inherits from db.Model and SerializerMixin
class Power(db.Model, SerializerMixin):
    # Name of fthe database table
    __tablename__ = "powers"

    # Prevent recursive serialization loops
    serialize_rules = ("-hero_powers.power",)

    # Table Columns with the id column as the primary key.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # Relationship to HeroPower join table
    hero_powers = db.relationship(
        "HeroPower",
        back_populates="power",
        cascade="all, delete-orphan"
    )

    # Validation for description field Ensure description exists and is at least 20 characters
    @validates("description")
    def validate_description(self, key, value):
        if not value or len(value) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return value

# HeroPower (Join table)
class HeroPower(db.Model, SerializerMixin):
    # Table name 
    __tablename__ = "hero_powers"

    # Prevent deep recursive serialization
    serialize_rules = ("-hero.hero_powers", "-power.hero_powers")

    # Table columns
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)

    # Foreign keys
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"))
    power_id = db.Column(db.Integer, db.ForeignKey("powers.id"))

    # Relationships back to Hero and power
    hero = db.relationship("Hero", back_populates="hero_powers")
    power = db.relationship("Power", back_populates="hero_powers")

    # Validation for strength field, Ensure strength is one of the allowed values
    @validates("strength")
    def validate_strength(self, key, value):
        if value not in ["Strong", "Weak", "Average"]:
            raise ValueError("Invalid strength")
        return value
