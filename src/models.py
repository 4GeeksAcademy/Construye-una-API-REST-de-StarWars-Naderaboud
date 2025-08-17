from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

favorite_characters_table = Table (
    "favourite_characters",

    db.metadata,
    db.Column("user_id", db.ForeignKey("user.id"), primary_key=True),
    db.Column("character_id", db.ForeignKey("character.id"), primary_key=True)
)

favorite_planets_table = Table(
    "favorite_planets",
    db.metadata,
    db.Column("user_id", db.ForeignKey("user.id"), primary_key=True),
    db.Column("planet_id", db.ForeignKey("planet.id"), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorite_characters: Mapped[List["Character"]] = relationship(
        "Character",
        secondary=favorite_characters_table,
        back_populates="favorited_by_users"
    )
    favorite_planets: Mapped[List["Planet"]] = relationship(
        "Planet",
        secondary=favorite_planets_table,
        back_populates="favorited_by_users"
    )


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    URL: Mapped[str] = mapped_column(String(), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    characters: Mapped[list["Character"]] = relationship("Character", back_populates="planet")

    favorited_by_users: Mapped[List[User]] = relationship(
        "User",
        secondary=favorite_planets_table,
        back_populates="favorite_planets"
    )

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "URL": self.URL,
            "description": self.description,
            "characters": self.characters
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(250), nullable=False)

    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)
    planet: Mapped["Planet"] = relationship("Planet", back_populates="characters")

    species_id: Mapped[int] = mapped_column(ForeignKey("species.id"), nullable=True)
    species: Mapped["Species"] = relationship("Species", back_populates="characters")

    favorited_by_users: Mapped[List[User]] = relationship(
        "User",
        secondary=favorite_planets_table,
        back_populates="favorite_characters"
    )

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "species": self.species.name,
            "description": self.description,
            "planet": self.planet,
        } 
    
class Species(db.Model):
    __tablename__ = "species"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    characters: Mapped[List["Character"]] = relationship("Character", back_populates="species")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }