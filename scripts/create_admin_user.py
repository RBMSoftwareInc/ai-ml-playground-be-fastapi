"""
Script to create admin users offline
Usage: python scripts/create_admin_user.py
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.auth import Role, UserRole

def truncate_password(password: str, max_bytes: int = 72) -> str:
    """Truncate password to max_bytes, handling UTF-8 encoding properly"""
    password_bytes = password.encode('utf-8')
    if len(password_bytes) <= max_bytes:
        return password
    # Truncate to max_bytes, but be careful with UTF-8 boundaries
    truncated = password_bytes[:max_bytes]
    # Try to decode, removing any incomplete character at the end
    try:
        return truncated.decode('utf-8')
    except UnicodeDecodeError:
        # Remove last byte(s) until we can decode
        while len(truncated) > 0:
            truncated = truncated[:-1]
            try:
                return truncated.decode('utf-8')
            except UnicodeDecodeError:
                continue
        return ""

def get_password_hash_safe(password: str) -> str:
    """Hash password with proper truncation and bcrypt error handling"""
    # Always truncate to 72 bytes first
    password = truncate_password(password, 72)
    
    # Try to use app.core.auth first
    try:
        from app.core.auth import get_password_hash
        return get_password_hash(password)
    except (ImportError, AttributeError, Exception) as e:
        # Fallback: use passlib directly, but handle bcrypt version issues
        try:
            # Import passlib context
            from passlib.context import CryptContext
            
            # Try to create context - this might fail with bcrypt version issues
            try:
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                return pwd_context.hash(password)
            except AttributeError as bcrypt_error:
                if "__about__" in str(bcrypt_error) or "bcrypt" in str(bcrypt_error).lower():
                    print("\n⚠️  Bcrypt version compatibility issue detected!")
                    print("   The bcrypt library version is incompatible with passlib.")
                    print("\n   To fix this, run:")
                    print("   pip install --upgrade bcrypt")
                    print("   OR")
                    print("   pip uninstall bcrypt && pip install bcrypt")
                    print("\n   Then try running this script again.")
                    raise Exception("Bcrypt compatibility error. Please update bcrypt.")
                raise
        except Exception as fallback_error:
            print(f"\n❌ Error initializing password hashing: {fallback_error}")
            raise

def create_admin_user(email: str, username: str, password: str, full_name: str = None):
    """Create an admin user with superuser privileges"""
    # Validate and truncate password length (bcrypt max is 72 bytes)
    password_bytes = password.encode('utf-8')
    original_len = len(password_bytes)
    
    if original_len > 72:
        print(f"⚠️  Warning: Password is {original_len} bytes, truncating to 72 bytes for bcrypt compatibility")
        password = truncate_password(password, 72)
        truncated_len = len(password.encode('utf-8'))
        print(f"   Truncated to {truncated_len} bytes")
    
    # Final validation
    final_bytes = len(password.encode('utf-8'))
    if final_bytes < 8:
        print("❌ Password too short! Minimum 8 bytes after truncation.")
        return False
    
    db: Session = SessionLocal()
    try:
        # Check if user exists
        existing_user = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            print(f"❌ User with email '{email}' or username '{username}' already exists")
            return False
        
        # Hash password with comprehensive error handling
        try:
            hashed_password = get_password_hash_safe(password)
        except Exception as hash_error:
            error_msg = str(hash_error)
            if "bcrypt" in error_msg.lower() or "__about__" in error_msg:
                print("\n❌ Bcrypt compatibility error!")
                print("\n   This is a known issue with bcrypt/passlib compatibility.")
                print("   Please run these commands to fix:")
                print("\n   cd ai-ml-playground-be-fastapi")
                print("   source venv/bin/activate")
                print("   pip install --upgrade bcrypt passlib")
                print("\n   Then try again.")
            else:
                print(f"\n❌ Error hashing password: {hash_error}")
                print("\n   Troubleshooting:")
                print("   1. Ensure you're in the virtual environment")
                print("   2. Try: pip install --upgrade passlib bcrypt")
            return False
        
        # Create user
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name or username,
            is_active=True,
            is_superuser=True,  # Make superuser
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Assign admin role if it exists
        admin_role = db.query(Role).filter(Role.role_name == "admin").first()
        if admin_role:
            user_role = UserRole(user_id=user.id, role_id=admin_role.id)
            db.add(user_role)
            db.commit()
            print(f"✅ Created admin user '{username}' with admin role")
        else:
            print(f"✅ Created superuser '{username}' (admin role not found, but is_superuser=True)")
        
        print(f"\n📧 Email: {email}")
        print(f"👤 Username: {username}")
        print(f"🔑 Password: {password[:20]}..." if len(password) > 20 else f"🔑 Password: {password}")
        print(f"\n⚠️  Save these credentials securely!")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating user: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    import getpass
    
    print("=" * 60)
    print("Create Admin User")
    print("=" * 60)
    print()
    
    email = input("Email: ").strip()
    if not email:
        print("❌ Email is required")
        sys.exit(1)
    
    username = input("Username: ").strip()
    if not username:
        print("❌ Username is required")
        sys.exit(1)
    
    password = getpass.getpass("Password: ").strip()
    if not password or len(password) < 8:
        print("❌ Password must be at least 8 characters")
        sys.exit(1)
    
    # Check password byte length (bcrypt limit is 72 bytes)
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        print(f"⚠️  Warning: Password is {len(password_bytes)} bytes.")
        print("   It will be truncated to 72 bytes for bcrypt compatibility.")
        print("   Consider using a shorter password to avoid truncation.")
        response = input("   Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            sys.exit(0)
    
    password_confirm = getpass.getpass("Confirm Password: ").strip()
    if password != password_confirm:
        print("❌ Passwords do not match")
        sys.exit(1)
    
    full_name = input("Full Name (optional): ").strip() or None
    
    print()
    success = create_admin_user(email, username, password, full_name)
    
    if success:
        print("\n✅ User created successfully!")
        print("\nYou can now login at: http://localhost:3000/admin/login")
    else:
        print("\n❌ Failed to create user")
        print("\nIf you're seeing bcrypt errors, try:")
        print("  cd ai-ml-playground-be-fastapi")
        print("  source venv/bin/activate")
        print("  pip install --upgrade bcrypt passlib")
        sys.exit(1)
