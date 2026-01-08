"""
Test script to verify all models can be imported and relationships work
Run this to check for database errors before running migrations
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test that all models can be imported"""
    print("Testing model imports...")
    try:
        from app.models import (
            User, Industry, UseCase, UseCaseCategory, UseCaseExecution,
            ContentAsset, Theme, ContentBlock, ActionDefinition,
            OutputTheme, AIModelConfiguration, ContentAuditLog,
            Role, Permission, UserRole, RolePermission, RefreshToken, LoginAttempt,
            WorkflowContentVersion, ContentApproval, WorkflowDefinition,
            ContentSchedule, CMSSettings, ContentStatus
        )
        print("✅ All models imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_relationships():
    """Test that relationships are properly defined"""
    print("\nTesting relationships...")
    try:
        from app.models.user import User
        from app.models.auth import UserRole, Role
        from app.models.cms_workflow import WorkflowContentVersion, ContentApproval
        
        # Check User model has user_roles relationship
        assert hasattr(User, 'user_roles'), "User should have user_roles relationship"
        print("✅ User relationships OK")
        
        # Check UserRole has user and role relationships
        assert hasattr(UserRole, 'user'), "UserRole should have user relationship"
        assert hasattr(UserRole, 'role'), "UserRole should have role relationship"
        print("✅ UserRole relationships OK")
        
        # Check WorkflowContentVersion has approvals
        assert hasattr(WorkflowContentVersion, 'approvals'), "WorkflowContentVersion should have approvals"
        print("✅ WorkflowContentVersion relationships OK")
        
        print("✅ All relationships verified")
        return True
    except Exception as e:
        print(f"❌ Relationship error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_base():
    """Test Base is working"""
    print("\nTesting Base...")
    try:
        from app.core.database import Base
        print("✅ Base imported successfully")
        return True
    except Exception as e:
        print(f"❌ Base error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Database Model Test Script")
    print("=" * 60)
    
    results = []
    results.append(("Base", test_base()))
    results.append(("Imports", test_imports()))
    results.append(("Relationships", test_relationships()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20} {status}")
    
    all_passed = all(r[1] for r in results)
    if all_passed:
        print("\n✅ All tests passed! Models are ready for migration.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Fix errors before running migrations.")
        sys.exit(1)

