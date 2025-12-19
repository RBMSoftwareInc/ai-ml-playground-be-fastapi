#!/usr/bin/env python3
"""
Install only packages from requirements.txt that are not already installed.
This avoids reinstalling packages that are already successfully installed.
"""
import subprocess
import sys
import re

def get_installed_packages():
    """Get a set of installed package names."""
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'list', '--format=freeze'],
        capture_output=True,
        text=True
    )
    installed = {}
    for line in result.stdout.strip().split('\n'):
        if '==' in line:
            name, version = line.split('==', 1)
            installed[name.lower()] = version
    return installed

def parse_requirement_line(line):
    """Parse a requirement line and return (package_name, version_spec)."""
    line = line.strip()
    # Skip comments and empty lines
    if not line or line.startswith('#'):
        return None, None
    
    # Remove comments at end of line
    if '#' in line:
        line = line[:line.index('#')].strip()
    
    # Parse package name and version spec
    # Handle cases like: package>=1.0.0, package==1.0.0, package~=1.0.0
    match = re.match(r'^([a-zA-Z0-9_-]+(?:\[[^\]]+\])?)(.*)$', line)
    if match:
        name = match.group(1)
        # Remove extras like [standard]
        name = re.sub(r'\[.*\]', '', name)
        version_spec = match.group(2).strip()
        return name, version_spec
    return None, None

def check_package_satisfies(installed_version, version_spec):
    """Check if installed version satisfies the version spec."""
    if not version_spec:
        return True
    
    # Simple check - if there's a version spec, we'll let pip handle it
    # For now, just return True if package is installed
    return installed_version is not None

def install_missing_packages(requirements_file='requirements.txt'):
    """Install only packages from requirements.txt that are missing."""
    installed = get_installed_packages()
    missing_packages = []
    
    print(f"Reading {requirements_file}...")
    try:
        with open(requirements_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {requirements_file} not found!")
        return
    
    for line_num, line in enumerate(lines, 1):
        name, version_spec = parse_requirement_line(line)
        if name is None:
            continue
        
        name_lower = name.lower()
        if name_lower not in installed:
            # Package not installed, add to missing list
            req_line = f"{name}{version_spec}" if version_spec else name
            missing_packages.append(req_line)
            print(f"  Line {line_num}: {req_line} - MISSING")
        else:
            print(f"  Line {line_num}: {name} - already installed ({installed[name_lower]})")
    
    if not missing_packages:
        print("\n✅ All packages are already installed!")
        return
    
    print(f"\n📦 Installing {len(missing_packages)} missing packages...")
    print("=" * 60)
    
    # Install missing packages one by one to avoid stopping on errors
    failed = []
    for package in missing_packages:
        print(f"\nInstalling: {package}")
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--upgrade-strategy', 'only-if-needed', package],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  ✅ Successfully installed {package}")
        else:
            print(f"  ❌ Failed to install {package}")
            print(f"  Error: {result.stderr[:200]}")
            failed.append(package)
    
    print("\n" + "=" * 60)
    if failed:
        print(f"\n⚠️  {len(failed)} packages failed to install:")
        for pkg in failed:
            print(f"   - {pkg}")
    else:
        print(f"\n✅ Successfully installed all {len(missing_packages)} missing packages!")

if __name__ == '__main__':
    requirements_file = sys.argv[1] if len(sys.argv) > 1 else 'requirements.txt'
    install_missing_packages(requirements_file)

