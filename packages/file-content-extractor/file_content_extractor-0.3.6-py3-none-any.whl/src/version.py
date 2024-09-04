import subprocess
import sys
import pkg_resources

PACKAGE_NAME = "file-content-extractor"

def get_version():
    try:
        version = pkg_resources.get_distribution(PACKAGE_NAME).version
    except pkg_resources.DistributionNotFound:
        version = "Version not found"
    return version

def check_for_updates():
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "--dry-run", PACKAGE_NAME],
                                capture_output=True, text=True)
        output = result.stdout
        current_version = get_version()
        latest_version = None

        for line in output.splitlines():
            if line.startswith("Collecting"):
                latest_version = line.split(' ')[1]
                break
        
        if latest_version and latest_version != current_version:
            print(f"Current version: {current_version}")
            print(f"Latest version: {latest_version}")
            upgrade = input("A new version is available. Would you like to upgrade now? [y]/n: ").strip().lower()
            if upgrade == 'n':
                return False, current_version
            else:
                upgrade_package()
                sys.exit(0)
        else:
            print(f"You are using the latest version: {current_version}")
            return False, current_version

    except Exception as e:
        print(f"Failed to check for updates: {e}")
        return False, get_version()

def upgrade_package():
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", PACKAGE_NAME], check=True)
        print("Package upgraded successfully.")
    except Exception as e:
        print(f"Failed to upgrade the package: {e}")
