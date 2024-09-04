# ssh
## 安装
```bash
pip3 install python3-ssh
```

## 使用
* 远程执行一条命令，比如 ls
```python
from ssh import SSHClient
ssh = SSHClient(ip="10.240.124.1",port=22,username="root",password="Mugen_runner@123456")
rs=ssh.exec("ls /")
# 执行命令的返回码
print(rs.exit_status_code)
# 执行命令的返回内容
print(rs.stdout)
```

