#!/usr/bin/env python

import argparse
import os
import getpass


if __name__=="__main__":

    user_name = getpass.getuser()
    default_image_name = user_name + '-tensorflow'

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", type=str,
                        help="(required) name of the image that this container is dervied from", default=default_image_name)

    parser.add_argument("-c", "--container", type=str, default="tensorflow", help="(optional) name of the container")

    parser.add_argument("-d", "--dry_run", action='store_true', help="(optional) perform a dry_run, print the command that would have been executed but don't execute it.")

    parser.add_argument("-p", "--passthrough", type=str, default="", help="(optional) extra string that will be tacked onto the docker run command, allows you to pass extra options")

    args = parser.parse_args()
    print "running docker container derived from image %s" %args.image
    source_dir=os.getcwd()

    
    image_name = args.image
    home_directory = '/home/' + user_name


    cmd = "xhost +local:root \n"
    cmd += "nvidia-docker run -it "
    if args.container:
        cmd += " --name %(container_name)s " % {'container_name': args.container}

    cmd += " -e DISPLAY -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v %(source_dir)s:%(home_directory)s/code "  % {'source_dir': source_dir, 'home_directory': home_directory}
    cmd += " -v ~/.ssh:%(home_directory)s/.ssh " % {'home_directory': home_directory}
    cmd += " --user %s " % user_name # login as current user

    # cmd += "xhost -local:root"
    # cmd += " -v /var/lib/docker/:/var/lib/docker " # for using perf inside the container
    cmd += " --privileged " # add privilege to this docker container, allows us to run perf inside container

    cmd += "  -p 8888:8888 "
    cmd += " --network=host "

    # following the suggestion here (https://stackoverflow.com/questions/44745987/use-perf-inside-a-docker-container-without-privileged)
    # for getting perf to run inside the docker container

    # seccompFile = os.path.join(source_dir, 'docker', "my-seccomp.json")
    # cmd += " --security-opt seccomp=" + seccompFile + " "
    # cmd += " --cap-add sys_admin "


    cmd += " --rm " # clean up the container on exit
    cmd += " " + args.passthrough + " "
    cmd += image_name + "\n"

    print "command = \n \n", cmd


    # build the docker image
    if not args.dry_run:
        print "executing shell command"
        os.system(cmd)
    else:
        print "dry run, not executing command"