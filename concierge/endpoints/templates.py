# -*- coding: utf-8 -*-


import datetime
import distutils.spawn
import os.path
import sys

import concierge


HEADER = """
# THIS FILE WAS AUTOGENERATED BY concierge on {date}.
# IT MAKES NO SENSE TO EDIT IT MANUALLY!
#
# CONCIERGERC FILE: {rc_file}
#
# PLEASE VISIT https://github.com/9seconds/concierge FOR DETAILS.
""".strip() + "\n\n"


SYSTEMD_CONFIG = """
[Unit]
Description=Daemon for converting ~/.concierge to ~/.ssh/config
After=syslog.target

[Service]
ExecStart={command} -u {templater} -o {sshconfig}
Restart=on-failure

[Install]
WantedBy=multi-user.target
""".strip()

SYSTEMD_SERVICE_NAME = "concierge.service"

SYSTEMD_INSTRUCTIONS = """
Please execute following lines or compose script:

$ mkdir -p "{systemd_user_path}" || true
$ cat > "{systemd_user_service_path}" <<EOF
{systemd_config}
EOF
$ systemctl --user enable {service_name}
$ systemctl --user start {service_name}
""".strip()


def make_header(**kwargs):
    return HEADER.format(
        date=kwargs.get("date", datetime.datetime.now().ctime()),
        rc_file=kwargs.get("rc_file", "???"))


def make_systemd_script(templater):
    systemd_user_path = os.path.join(concierge.HOME_DIR,
                                     ".config", "systemd", "user")
    systemd_user_service_path = os.path.join(systemd_user_path,
                                             SYSTEMD_SERVICE_NAME)
    systemd_config = SYSTEMD_CONFIG.format(
        command=distutils.spawn.find_executable(sys.argv[0]),
        sshconfig=concierge.DEFAULT_SSHCONFIG,
        templater=templater.name.lower())

    yield 'mkdir -p "{0}" || true'.format(systemd_user_path)
    yield 'cat > "{0}" <<EOF\n{1}\nEOF'.format(systemd_user_service_path,
                                               systemd_config.strip())
    yield "systemctl --user enable {0}".format(SYSTEMD_SERVICE_NAME)
    yield "systemctl --user start {0}".format(SYSTEMD_SERVICE_NAME)
