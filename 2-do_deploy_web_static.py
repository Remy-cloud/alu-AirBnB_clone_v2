#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ["3.84.95.54", "3.82.241.91"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        release_path = "/data/web_static/releases/{}".format(name)

        # Upload archive to /tmp/ on the remote server
        put(archive_path, "/tmp/")

        # Create release directory
        run("mkdir -p {}".format(release_path))

        # Uncompress archive to the release folder
        run("tar -xzf /tmp/{} -C {}".format(file_name, release_path))

        # Remove uploaded archive
        run("rm /tmp/{}".format(file_name))

        # Move contents from web_static/ to the release path
        run("mv {0}/web_static/* {0}/".format(release_path))

        # Remove now-empty web_static directory
        run("rm -rf {}/web_static".format(release_path))

        # Remove the old symlink and create a new one
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))

        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False
