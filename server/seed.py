
from app import app, db
from models import Hero, Power, HeroPower

with app.app_context():
    Hero.query.delete()
    Power.query.delete()
    HeroPower.query.delete()

    
    # --- Create Heroes ---
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

    heroes = []
    for name, super_name in hero_data:
        heroes.append(Hero(name=name, super_name=super_name))
    db.session.add_all(heroes)
    db.session.commit()

    # --- Create Powers ---
    power_data = [
        ("super strength", "gives the wielder super-human strengths"),
        ("flight", "gives the wielder the ability to fly through the skies at supersonic speed"),
        ("super human senses", "allows the wielder to use her senses at a super-human level"),
        ("elasticity", "can stretch the human body to extreme lengths")
    ]

    powers = []
    for name, description in power_data:
        powers.append(Power(name=name, description=description))
    db.session.add_all(powers)
    db.session.commit()

    # --- Assign Hero Powers (exactly as rubric expects) ---
    # Format: (hero_id, power_id, strength)
    hero_power_data = [
        (1, 2, "Strong"),  # Kamala Khan - flight
        (2, 1, "Average"), # Doreen Green - super strength
        (3, 3, "Strong"),  # Gwen Stacy - super human senses
        (4, 4, "Weak"),    # Janet Van Dyne - elasticity
        (5, 1, "Strong"),  # Wanda Maximoff - super strength
        (6, 2, "Average"), # Carol Danvers - flight
        (7, 1, "Strong"),  # Jean Grey - super strength
        (8, 3, "Average"), # Ororo Munroe - super human senses
        (9, 1, "Weak"),    # Kitty Pryde - super strength
        (10, 3, "Strong")  # Elektra - super human senses
    ]

    hero_powers = []
    for hero_id, power_id, strength in hero_power_data:
        hero_powers.append(HeroPower(hero_id=hero_id, power_id=power_id, strength=strength))
    db.session.add_all(hero_powers)
    db.session.commit()

