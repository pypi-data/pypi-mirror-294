import os
import subprocess
import paramiko
from log import log
from func_timeout import func_set_timeout
from func_timeout.exceptions import FunctionTimedOut
from paramiko.ssh_exception import SSHException


class ExecResult():
    def __init__(self, exit_status_code, stdout="", stderr=""):
        self.__exit_status_code = exit_status_code
        self.__stdout = stdout
        self.__stderr = stderr

    @property
    def exit_status_code(self):
        return self.__exit_status_code

    @property
    def stdout(self):
        return self.__stdout

    @property
    def stderr(self):
        return self.__stderr


class SSHClient(object):
    def __init__(self, ip="127.0.0.1", port=22, username="root", password="", connect_timeout=30):
        self.__ip = ip
        self.__port = port
        self.__username = username
        self.__password = password
        self.__connect_timeout = connect_timeout
        self.__ssh = paramiko.SSHClient()
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__is_active = False
        self.__sftp = None

    def __del__(self):
        try:
            self.__sftp.close()
        except:
            pass
        try:
            self.__ssh.close()
        except:
            pass

    @func_set_timeout(int(os.environ.get("SSH_COMMAND_TIMEOUT", 60)))
    def _exec(self, cmd, promt_response):
        log.info(f" {self.__ip}:{self.__port} | begin to run cmd:{cmd}.")
        try:
            if promt_response:
                channel = self.__ssh.get_transport().open_session()
                channel.get_pty()  # 获取虚拟终端
                channel.exec_command(cmd)
                output = ""
                while not channel.closed or channel.recv_ready() or channel.recv_stderr_ready():
                    if channel.recv_ready():
                        output = channel.recv(1024).decode('utf-8', 'ignore')
                        print(output, end='')

                        # 检查输出是否包含预期的提示信息
                        for elem in promt_response:
                            prompt = elem["prompt"]
                            response = elem["response"]
                            if prompt in output:
                                # 发送相应的回答
                                channel.send(response)
                    if channel.recv_stderr_ready():
                        print(channel.recv_stderr(2024).decode('utf-8', 'ignore'), end='')

                return_code = channel.recv_exit_status()
                return ExecResult(return_code, output, "")
            else:
                stdin, stdout, stderr = self.__ssh.exec_command(cmd)
                exit_status = stdout.channel.recv_exit_status()
                std_output = stdout.read().decode()
                std_err = stderr.read().decode()
                log.info(
                    f" {self.__ip}:{self.__port} | successful to run cmd {cmd}, output is:{std_output}.")
                return ExecResult(exit_status, std_output, std_err)
        except Exception as e:
            return ExecResult(255, "", str(e))

    def exec(self, cmd, promt_response=[], timeout=60):
        try:
            os.environ["SSH_COMMAND_TIMEOUT"] = str(timeout)
            if not self.is_active():
                raise RuntimeError("ssh transport is not active.")
            return self._exec(cmd,promt_response)
        except FunctionTimedOut as e1:
            log.error(f"when run cmd: {cmd}, meets exception.", exc_info=True)
            return ExecResult(1, "", str(e1))
        except Exception as e:
            log.error(f"when run cmd: {cmd}, meets exception.", exc_info=True)
            return ExecResult(1, "", str(e))

    @func_set_timeout(int(os.environ.get("SSH_SCP_TO_REMOTE_TIMEOUT", 120)))
    def _scp_to_remote(self, local_path, remote_path):
        log.info(
            f" {self.__ip}:{self.__port} | Begin to copy file from local {local_path} to remote host {remote_path}.")
        self.__sftp.put(local_path, remote_path)
        rs = self.exec(f"ls {remote_path}")
        if rs.exit_status_code == 0:
            log.info(
                f" {self.__ip}:{self.__port} | Success to copy file from local {local_path} to remote host{remote_path}: OK.")
            return True
        else:
            log.error(
                f" {self.__ip}:{self.__port} | failed to copy file from local {local_path} to remote host{remote_path}:Error.")
            return False

    def scp_to_remote(self, local_path, remote_path,timeout=120):
        try:
            if not self.is_active():
                raise RuntimeError("ssh transport is not active.")
            os.environ["SSH_SCP_TO_REMOTE_TIMEOUT"] = str(timeout)
            return self._scp_to_remote(local_path, remote_path)
        except RuntimeError:
            log.error(
                f"{self.__ip}:{self.__port} | failed to run copy file from local {local_path} to remote {remote_path} for ssh transport is not active..",
                exc_info=True)
            return False
        except TimeoutError:
            log.error(
                f"{self.__ip}:{self.__port} | timeout to run copy file from local {local_path} to remote {remote_path}.",
                exc_info=True)
            return False
        except Exception:
            log.error(f"when scp from local {local_path} to remote {remote_path}, meets exception.", exc_info=True)
            return False

    @func_set_timeout(int(os.environ.get("SSH_SCP_FILE_TO_LOCAL_TIMEOUT",120)))
    def _scp_file_to_local(self, remote_path, local_path):
        log.info(
            f" {self.__ip}:{self.__port} | Begin to copy file from remote {remote_path} to local host {local_path}.")
        if os.path.isfile(local_path):
            subprocess.run(['rm', '-rf', local_path], capture_output=True, text=True)
        self.__sftp.get(remote_path, local_path)
        rs = subprocess.Popen(['ls', local_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if rs.returncode == 0:
            log.info(
                f" {self.__ip}:{self.__port} | Success to copy file from remote {remote_path} to local host{local_path}:OK.")
            return True
        else:
            log.error(
                f" {self.__ip}:{self.__port} | failed to copy file from remote {remote_path} to local host{local_path}:Error.")
            return False

    def scp_file_to_local(self, remote_path, local_path,timeout=120):
        try:
            if not self.is_active():
                raise RuntimeError("ssh transport is not active.")
            os.environ["SSH_SCP_FILE_TO_LOCAL_TIMEOUT"] = str(timeout)
            return self._scp_file_to_local(remote_path, local_path)
        except RuntimeError:
            log.error(
                f"{self.__ip}:{self.__port} | failed to copy file from remote {remote_path} to local {local_path} for ssh transport is not active.",
                exc_info=True)
            return False
        except TimeoutError:
            log.error(
                f"{self.__ip}:{self.__port} | timeout to run copy file from remote {remote_path} to local {local_path}.",
                exc_info=True)
            return False
        except Exception:
            log.error(f"when scp from remote {remote_path} to local {local_path}, meets exception.", exc_info=True)
            return False

    def is_active(self):
        for i in range(2):
            try:
                if not self.__is_active:
                    log.info(f" {self.__ip}:{self.__port} | begin to create ssh connect.")
                    self.__ssh.connect(
                        self.__ip,
                        port=self.__port,
                        username=self.__username,
                        password=self.__password,
                        look_for_keys=False,
                        allow_agent=False,
                        timeout=self.__connect_timeout
                    )

                stdin, stdout, stderr = self.__ssh.exec_command("ls /")
                std_output = stdout.read().decode()
                if "root" in std_output:
                    log.info(f"{self.__ip}:{self.__port} | successful to ssh:OK.")
                    self.__sftp = self.__ssh.open_sftp()
                    self.__is_active = True
                    return True
                else:
                    log.warning(f"{self.__ip}:{self.__port} | failed to ssh. stderr is {stderr.read().decode()}.")
                    self.__is_active = False
            except SSHException:
                log.warning(f" {self.__ip}:{self.__port} | fail create ssh connect.")
                self.__is_active = False
            except Exception:
                log.warning(f" {self.__ip}:{self.__port} | fail create ssh connect.")
                self.__is_active = False
        return False
