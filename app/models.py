from .db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy import event, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.associationproxy import association_proxy

# Model to track the next human-readable ID for each table
class HumanIdSequence(db.Model):
    __tablename__ = 'human_id_sequence'
    model_name = db.Column(db.String(100), primary_key=True)
    next_value = db.Column(db.Integer, nullable=False, default=1)

# Abstract base model providing common fields
class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    human_id = db.Column(db.Integer, unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_updated_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)

# --- SQLAlchemy Event Listener for human_id generation ---

@event.listens_for(BaseModel, 'before_insert', propagate=True)
def generate_human_id(mapper, connection, target):
    """
    Listen for the 'before_insert' event and generate a human_id.
    This replicates the logic from the Django example using SQLAlchemy events.
    """
    model_class = target.__class__
    model_name = model_class.__name__

    # Lock the sequence row for this model to prevent race conditions
    sequence_row = connection.execute(
        db.select(HumanIdSequence).filter_by(model_name=model_name).with_for_update()
    ).first()

    if sequence_row:
        next_id = sequence_row.next_value
        # Increment the sequence for the next insert
        connection.execute(
            db.update(HumanIdSequence)
            .where(HumanIdSequence.model_name == model_name)
            .values(next_value=next_id + 1)
        )
    else:
        # If no sequence exists for this model, create one
        next_id = 1
        connection.execute(
            db.insert(HumanIdSequence).values(model_name=model_name, next_value=2)
        )

    target.human_id = next_id

# --- Application Models ---

class UserRole(BaseModel):
    __tablename__ = 'user_roles'
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id'), primary_key=True)

    # Bidirectional relationship with User and Role
    user = db.relationship("User", back_populates="role_associations", foreign_keys=[user_id])
    role = db.relationship("Role", back_populates="user_associations")

    def __repr__(self):
        # Check if user and role are loaded to avoid lazy loading issues in repr
        user_name = self.user.name if self.user else "N/A"
        role_name = self.role.name if self.role else "N/A"
        return f"<UserRole user={user_name} role={role_name}>"

class Role(BaseModel):
    __tablename__ = 'roles'
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Relationship to the association object
    user_associations = db.relationship("UserRole", back_populates="role", cascade="all, delete-orphan")

    # Proxy for easy access to users, so we can still do role.users
    users = association_proxy('user_associations', 'user')

    def __repr__(self):
        return f"<Role {self.name}>"


# Association table for many-to-many User <-> Team with summary
class TeamMembership(db.Model):
    __tablename__ = 'team_memberships'
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True)
    team_id = db.Column(UUID(as_uuid=True), db.ForeignKey('teams.id'), primary_key=True)
    summary = db.Column(db.String(255), nullable=True)  # User's role/summary in the team
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = db.relationship('User', back_populates='team_associations')
    team = db.relationship('Team', back_populates='user_associations')

class Team(BaseModel):
    __tablename__ = 'teams'
    name = db.Column(db.String(150), nullable=False)
    manager_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)

    # Relationship to the association object
    user_associations = db.relationship('TeamMembership', back_populates='team', cascade='all, delete-orphan')
    members = association_proxy('user_associations', 'user')

    # Relationship to manager (User)
    manager = db.relationship('User', back_populates='managed_teams', foreign_keys=[manager_id])

    def __repr__(self):
        return f"<Team {self.name}>"

class User(BaseModel):
    __tablename__ = 'users'
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)

    # Individual manager (User)
    manager_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)
    team_members = db.relationship(
        'User',
        backref=db.backref('manager', remote_side='User.id'),
        lazy='dynamic',
        foreign_keys='User.manager_id'
    )

    # Relationship to the association object for roles
    role_associations = db.relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys=[UserRole.user_id]
    )
    roles = association_proxy('role_associations', 'role')

    # Relationship to the association object for teams
    team_associations = db.relationship('TeamMembership', back_populates='user', cascade='all, delete-orphan')
    teams = association_proxy('team_associations', 'team')

    # Teams this user manages
    managed_teams = db.relationship('Team', back_populates='manager', foreign_keys='Team.manager_id')

    def __repr__(self):
        return f"<User {self.email}>"
