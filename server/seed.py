## Import the Flask app and database instance
from app import app, db
# Import models
from models import Hero, Power, HeroPower

# Use app context to allow database operations
with app.app_context():

    # Delete all records to avoid duplication when reseeding
    HeroPower.query.delete()
    Hero.query.delete()
    Power.query.delete()
    

    
    # Create Heroes 
    hero_data = [
        ("Kamala Khan", "Ms. Marvel"),
        ("Doreen Green", "Squirrel Girl"),
        ("Gwen Stacy", "Spider-Gwen"),
        ("Janet Van Dyne", "The Wasp"),
        ("Wanda Maximoff", "Scarlet Witch"),
        ("Carol Danvers", "Captain Marvel"),
        ("Jean Grey", "Dark Phoenix"),
        ("Ororo Munroe", "Storm"),
        ("Kitty Pryde", "Shadowcat"),
        ("Elektra Natchios", "Elektra")
    ]

    # Create Hero objects
    heroes = []
    for name, super_name in hero_data:
        heroes.append(Hero(name=name, super_name=super_name))
    # Add heroes to the database
    db.session.add_all(heroes)
    # Commits heroes to db 
    db.session.commit()

    # Create Powers 
    power_data = [
        ("super strength", "gives the wielder super-human strengths"),
        ("flight", "gives the wielder the ability to fly through the skies at supersonic speed"),
        ("super human senses", "allows the wielder to use her senses at a super-human level"),
        ("elasticity", "can stretch the human body to extreme lengths")
    ]

    # Create Power objects
    powers = []
    for name, description in power_data:
        powers.append(Power(name=name, description=description))

    # Add powers to the database
    db.session.add_all(powers)
    db.session.commit()

    # Assign Hero Powers 
    # Format: (hero_id, power_id, strength)
    hero_power_data = [
        (1, 2, "Strong"),  
        (2, 1, "Average"),
        (3, 3, "Strong"),  
        (4, 4, "Weak"),    
        (5, 1, "Strong"),  
        (6, 2, "Average"), 
        (7, 1, "Strong"),  
        (8, 3, "Average"), 
        (9, 1, "Weak"),    
        (10, 3, "Strong")  
    ]

     # Create HeroPower objects
    hero_powers = []
    for hero_id, power_id, strength in hero_power_data:
        hero_powers.append(HeroPower(hero_id=hero_id, power_id=power_id, strength=strength))

    # Add hero powers to the database
    db.session.add_all(hero_powers)
    db.session.commit()

