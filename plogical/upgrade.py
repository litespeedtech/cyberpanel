import thread
import tarfile
import os
import shlex
import subprocess
import shutil
import requests
import json
import platform

system=platform.dist()[0]
version=float(platform.dist()[1])


class Upgrade:
    logPath = "/usr/local/lscp/logs/upgradeLog"

    @staticmethod
    def downloadLink():
        url = "https://cyberpanel.net/version.txt"
        r = requests.get(url, verify=True)
        data = json.loads(r.text)
        version_number = str(data['version'])
        version_build = str(data['build'])
        return (version_number + "." + version_build + ".tar.gz")



    @staticmethod
    def upgrade():

        os.chdir("/usr/local")

        versionNumbring = Upgrade.downloadLink()

        ## Download latest version.

        command = "wget https://cyberpanel.net/CyberPanel." + versionNumbring
        subprocess.call(shlex.split(command))

        ## Backup settings file.

        shutil.copy("/usr/local/CyberCP/CyberCP/settings.py","/usr/local/settings.py")

        ## Remove Core Files

        command = "rm -rf /usr/local/CyberCP"
        subprocess.call(shlex.split(command))

        ## Extract Latest files

        command = "tar zxf CyberPanel." + versionNumbring
        subprocess.call(shlex.split(command))

        ## Copy settings file

        shutil.copy("/usr/local/settings.py", "/usr/local/CyberCP/CyberCP/")

        ## Move static files

        command = "rm -rf /usr/local/lscp/cyberpanel/static"
        subprocess.call(shlex.split(command))

        command = "mv /usr/local/CyberCP/static /usr/local/lscp/cyberpanel"
        subprocess.call(shlex.split(command))

        ## Copy File manager files

        command = "rm -rf /usr/local/lsws/Example/html/FileManager"
        subprocess.call(shlex.split(command))

        command = "mv /usr/local/CyberCP/install/FileManager /usr/local/lsws/Example/html"
        subprocess.call(shlex.split(command))


        ## Install TLDExtract

        command = "pip install tldextract"
        subprocess.call(shlex.split(command))

        ## Change File manager permissions

        command = "chmod -R 777 /usr/local/lsws/Example/html/FileManager"
        subprocess.call(shlex.split(command))

        ## Restart Gunicorn

        if version >= 7:
            command = "sudo systemctl restart gunicorn.socket"
        elif version >= 6:
            command = "sudo service gunicorn restart"
        subprocess.call(shlex.split(command))

        ## Upgrade version

        r = requests.post("http://localhost:5003/base/upgradeVersion")


        print("Upgrade Completed.")

Upgrade.upgrade()