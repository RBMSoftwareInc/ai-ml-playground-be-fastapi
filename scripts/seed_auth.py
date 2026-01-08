"""
Seed script for authentication system
Creates default roles, permissions, and optionally a superuser
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.auth import Role, Permission, RolePermission, UserRole
from app.core.auth import get_password_hash

# Default permissions by resource
PERMISSIONS = [
    # Content permissions
    {"name": "content.create", "display": "Create Content", "resource": "content", "action": "create"},
    {"name": "content.read", "display": "Read Content", "resource": "content", "action": "read"},
    {"name": "content.update", "display": "Update Content", "resource": "content", "action": "update"},
    {"name": "content.delete", "display": "Delete Content", "resource": "content", "action": "delete"},
    {"name": "content.publish", "display": "Publish Content", "resource": "content", "action": "publish"},
    {"name": "content.approve", "display": "Approve Content", "resource": "content", "action": "approve"},
    
    # Theme permissions
    {"name": "theme.create", "display": "Create Theme", "resource": "theme", "action": "create"},
    {"name": "theme.read", "display": "Read Theme", "resource": "theme", "action": "read"},
    {"name": "theme.update", "display": "Update Theme", "resource": "theme", "action": "update"},
    {"name": "theme.delete", "display": "Delete Theme", "resource": "theme", "action": "delete"},
    
    # Asset permissions
    {"name": "asset.upload", "display": "Upload Asset", "resource": "asset", "action": "upload"},
    {"name": "asset.read", "display": "Read Asset", "resource": "asset", "action": "read"},
    {"name": "asset.delete", "display": "Delete Asset", "resource": "asset", "action": "delete"},
    
    # AI Model permissions
    {"name": "ai_model.configure", "display": "Configure AI Model", "resource": "ai_model", "action": "configure"},
    {"name": "ai_model.train", "display": "Train AI Model", "resource": "ai_model", "action": "train"},
    {"name": "ai_model.deploy", "display": "Deploy AI Model", "resource": "ai_model", "action": "deploy"},
    
    # User management
    {"name": "user.read", "display": "Read Users", "resource": "user", "action": "read"},
    {"name": "user.manage", "display": "Manage Users", "resource": "user", "action": "manage"},
    
    # Role management
    {"name": "role.read", "display": "Read Roles", "resource": "role", "action": "read"},
    {"name": "role.manage", "display": "Manage Roles", "resource": "role", "action": "manage"},
    
    # Settings
    {"name": "settings.read", "display": "Read Settings", "resource": "settings", "action": "read"},
    {"name": "settings.update", "display": "Update Settings", "resource": "settings", "action": "update"},
]

# Default roles with their permissions
ROLES = [
    {
        "name": "admin",
        "display": "Administrator",
        "description": "Full access to all CMS features",
        "permissions": ["content.*", "theme.*", "asset.*", "ai_model.*", "user.*", "role.*", "settings.*"],
        "is_system": True,
    },
    {
        "name": "editor",
        "display": "Content Editor",
        "description": "Can create and edit content, submit for review",
        "permissions": ["content.create", "content.read", "content.update", "theme.read", "asset.upload", "asset.read"],
        "is_system": True,
    },
    {
        "name": "reviewer",
        "display": "Content Reviewer",
        "description": "Can review and approve content",
        "permissions": ["content.read", "content.approve", "content.publish"],
        "is_system": True,
    },
    {
        "name": "viewer",
        "display": "Viewer",
        "description": "Read-only access",
        "permissions": ["content.read", "theme.read", "asset.read"],
        "is_system": True,
    },
]


def seed_permissions(db: Session):
    """Create all permissions"""
    print("Creating permissions...")
    created = 0
    
    for perm_data in PERMISSIONS:
        existing = db.query(Permission).filter(Permission.permission_name == perm_data["name"]).first()
        if not existing:
            permission = Permission(
                permission_name=perm_data["name"],
                display_name=perm_data["display"],
                resource=perm_data.get("resource"),
                action=perm_data.get("action"),
            )
            db.add(permission)
            created += 1
            print(f"  ✓ Created permission: {perm_data['name']}")
    
    db.commit()
    print(f"✅ Created {created} permissions")
    return created


def seed_roles(db: Session):
    """Create roles and assign permissions"""
    print("\nCreating roles...")
    created = 0
    
    # Get all permissions
    all_permissions = {p.permission_name: p for p in db.query(Permission).all()}
    
    for role_data in ROLES:
        role = db.query(Role).filter(Role.role_name == role_data["name"]).first()
        if not role:
            role = Role(
                role_name=role_data["name"],
                display_name=role_data["display"],
                description=role_data.get("description"),
                is_system=role_data.get("is_system", False),
            )
            db.add(role)
            db.commit()
            db.refresh(role)
            created += 1
            print(f"  ✓ Created role: {role_data['display']}")
        else:
            print(f"  - Role already exists: {role_data['display']}")
        
        # Assign permissions
        permission_names = role_data.get("permissions", [])
        for perm_name in permission_names:
            # Handle wildcard permissions (e.g., "content.*")
            if perm_name.endswith(".*"):
                prefix = perm_name[:-2]
                matching_perms = [p for name, p in all_permissions.items() if name.startswith(prefix + ".")]
            else:
                matching_perms = [all_permissions.get(perm_name)] if perm_name in all_permissions else []
            
            for perm in matching_perms:
                if perm:
                    existing = db.query(RolePermission).filter(
                        RolePermission.role_id == role.id,
                        RolePermission.permission_id == perm.id
                    ).first()
                    
                    if not existing:
                        role_perm = RolePermission(role_id=role.id, permission_id=perm.id)
                        db.add(role_perm)
        
        db.commit()
    
    print(f"✅ Created {created} roles")
    return created


def create_superuser(db: Session, email: str = "admin@example.com", password: str = "admin123", username: str = "admin"):
    """Create a superuser account"""
    print(f"\nCreating superuser: {email}")
    
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        print(f"  - User already exists: {email}")
        return existing
    
    user = User(
        email=email,
        username=username,
        hashed_password=get_password_hash(password),
        full_name="Super Admin",
        is_active=True,
        is_superuser=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    print(f"  ✓ Created superuser: {email}")
    print(f"  ⚠️  Default password: {password} - CHANGE THIS IN PRODUCTION!")
    return user


def main():
    """Main seeding function"""
    db = SessionLocal()
    try:
        print("=" * 60)
        print("Seeding Authentication System")
        print("=" * 60)
        
        seed_permissions(db)
        seed_roles(db)
        
        # Create superuser (optional - comment out if not needed)
        import os
        admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        create_superuser(db, admin_email, admin_password)
        
        print("\n" + "=" * 60)
        print("✅ Authentication system seeded successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

