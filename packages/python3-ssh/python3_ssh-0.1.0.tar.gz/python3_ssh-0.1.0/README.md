# ssh
## 安装
```bash
pip3 install python3-ssh
```

## 用法
* 执行一条简单的命令，并获取执行命令的返回码、标准输出和标准错误
远程执行一条简单的命令，比如 ls，调试时需要将ip地址和用户名密码修改为自己的调试环境的信息
```python
from ssh.ssh import SSHClient


if __name__ == '__main__':
    ssh = SSHClient(ip="192.168.1.2", port=22, username="root", password="xxxx")
    rs = ssh.exec("ls /")
    print(f"exit_status_code:{rs.exit_status_code}")
    print(f"stdout:{rs.stdout}")
    print(f"stderr:{rs.stderr}")
```
执行结果如下：
```bash
exit_status_code:0
stdout:afs
bin
boot
dev
etc
home
lib
lib64
lost+found
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var

stderr:
```

