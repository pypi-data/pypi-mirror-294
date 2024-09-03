import unittest
from ssh.ssh import SSHClient

class TestSSH(unittest.TestCase):
    def test_ssh_exec(self):
        ssh = SSHClient(ip="10.240.124.1",port=22,username="root",password="Mugen_runner@123456")
        rs=ssh.exec("ls /")
        assert rs.exit_status_code == 0
        assert "root" in rs.stdout


if __name__ == '__main__':
    unittest.main()
