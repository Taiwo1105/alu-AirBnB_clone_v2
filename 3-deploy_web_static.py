#!/usr/bin/env python3
from fabric.api import env, run, put, local
import os
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with actual IP addresses of your web servers

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None

def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = os.path.basename(archive_path)
        no_ext = file_name.split('.')[0]
        path = "/data/web_static/releases/{}/".format(no_ext)

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Create the directory where the archive will be unpacked
        run("mkdir -p {}".format(path))

        # Unpack the archive to the folder on the web server
        run("tar -xzf /tmp/{} -C {}".format(file_name, path))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))

        # Move the unpacked content to the correct location
        run("mv {}web_static/* {}".format(path, path))

        # Remove the now empty web_static folder
        run("rm -rf {}web_static".format(path))

        # Delete the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new deployment
        run("ln -s {} /data/web_static/current".format(path))

        return True
    except Exception as e:
        return False

def deploy():
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

