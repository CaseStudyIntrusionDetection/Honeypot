import logging
import telnetlib
from shlex import quote

from tanner.config import TannerConfig

class AIODockerHelper:
    def __init__(self):

        self.logger = logging.getLogger('tanner.aiodocker_helper.AIODockerHelper')

        self.host = TannerConfig.get('ALPINE', 'hostname')
        self.user = TannerConfig.get('ALPINE', 'username')
        self.password = TannerConfig.get('ALPINE', 'password')

    async def execute_cmd(self, cmd):
        """
        Connects to the execution docker container via telnet and executes command
        :param cmd (list): contains commands to run in the container. ex: ["sh", "-c", "echo 'Hello'"]
        :return: execute_result (str): execution output/errors of cmd from the container
        """

        # build command
        cmd[2] = quote(cmd[2])
        cmd = (" ".join(cmd) + "\n")

        # connect and login
        tn = telnetlib.Telnet(self.host)
        tn.read_until(b"login: ")
        tn.write(self.user.encode('ascii') + b"\n")
        tn.read_until(b"Password: ")
        tn.write(self.password.encode('ascii') + b"\n")

        # run command
        tn.write(cmd.encode('ascii'))

        # exit and read data
        tn.write(b"exit\n")
        response = tn.read_all().decode('ascii')
        
        # parse
        start = response.find("$ " + cmd.strip()) + len("$ " + cmd.strip())
        end = response.rfind("\n", 0, response.rfind("exit"))

        return response[start:end].strip()
