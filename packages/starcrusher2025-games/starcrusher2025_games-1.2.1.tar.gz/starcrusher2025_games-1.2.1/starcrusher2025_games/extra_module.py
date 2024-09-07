import pip
import subprocess
import requests
import pkg_resources

def get_installed_version(package_name):
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return None

def get_latest_version(package_name):
    response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
    if response.status_code == 200:
        data = response.json()
        return data['info']['version']
    return None

def notify_user_if_update_available(package_name):
    print('searching for update')
    installed_version = get_installed_version(package_name)
    latest_version = get_latest_version(package_name)
    OKGREEN = '\033[92m'

    if installed_version and latest_version:
        if installed_version != latest_version:
            print('\033[93m' + f"Update available for {package_name}: {installed_version} -> {latest_version}. Use " + '\033[4m' + f"pip install --upgrade {package_name}" + '\033[0m' + '\033[93m' + " to update the package" + '\033[0m')
        else:
            print('\033[92m' + f"{package_name} is up-to-date (version {installed_version})." + '\033[0m')
    elif not installed_version:
        print('\033[91m' + f"{package_name} is not installed." + '\033[0m')
        print()
        print("how did you manage to do this???")
        print()
    else:
        print('\033[91m' + f"Could not fetch the latest version for {package_name}." + '\033[0m')