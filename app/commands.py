import click
from flask.cli import with_appcontext
from app.models import Role, db

@click.command('create-roles')
@with_appcontext
def create_roles_command():
    roles = ["Manager", "Chef", "Waiter", "Cleaner", "Bar staff"]
    created = []
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            db.session.add(Role(name=role_name))
            created.append(role_name)
    db.session.commit()
    if created:
        click.echo(f"Created roles: {', '.join(created)}")
    else:
        click.echo("All roles already exist.")
