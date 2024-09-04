# Your Python script logic goes here
import os
import subprocess
import sys

def is_java_installed(version):
    java_home = f"C:\\Program Files\\Java\\{version}"
    return os.path.exists(java_home)

def set_java_version(version):
    java_home = f"C:\\Program Files\\Java\\{version}"
    if not is_java_installed(version):
        print(f"Java version {version} is not installed.")
        return False
    
    os.environ["JAVA_HOME"] = java_home
    
    # Update system Path
    old_path = os.environ["Path"]
    new_path = ";".join(p for p in old_path.split(";") if "C:\\Program Files\\Java\\jdk" not in p)
    new_path += f";{java_home}\\bin"
    os.environ["Path"] = new_path

    # Set JAVA_HOME and Path for the current user
    subprocess.run([
        "setx", "JAVA_HOME", java_home, "/M"
    ], shell=True)
    
    subprocess.run([
        "setx", "Path", new_path, "/M"
    ], shell=True)
    
    print(f"Switched to Java version: {version}")
    return True

def get_installed_java_versions():
    java_base_path = "C:\\Program Files\\Java"
    if not os.path.exists(java_base_path):
        return []
    return [d for d in os.listdir(java_base_path) if os.path.isdir(os.path.join(java_base_path, d))]

def main():
    java_versions = get_installed_java_versions()
    
    if not java_versions:
        print("No Java versions installed.")
        sys.exit(1)
    
    print("Installed Java versions:")
    for i, version in enumerate(java_versions, start=1):
        print(f"{i}. {version}")
    
    choice = input(f"Enter the number corresponding to the Java version you want to use (1-{len(java_versions)}): ")
    
    try:
        selected_version = java_versions[int(choice) - 1]
    except (IndexError, ValueError):
        print("Invalid selection.")
        sys.exit(1)
    
    if not set_java_version(selected_version):
        print("Please install the desired Java version and try again.")
    
    # Verify the change
    subprocess.run(["java", "-version"], shell=True)

if __name__ == "__main__":
    main()
