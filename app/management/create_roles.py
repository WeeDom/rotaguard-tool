from app import create_app, db
from app.models import Role

ROLES = [
    "Manager",
    "Chef",
    "Waiter",
    "Cleaner",
    "Bar staff"
]

def create_roles():
    app = create_app()
    with app.app_context():
        created = []
        for role_name in ROLES:
            if not Role.query.filter_by(name=role_name).first():
                db.session.add(Role(name=role_name))
                created.append(role_name)
        db.session.commit()
        if created:
            print(f"Created roles: {', '.join(created)}")
        else:
            print("All roles already exist.")

if __name__ == "__main__":
    create_roles()
