import paramiko
from pathlib import Path

# ==== НАСТРОЙКИ ====
host = "45.139.77.206"
port = 22
username = "root"
password = "pGjx7HPCsgdm3#"  # или использовать ключ
local_file = Path("sait/main/static/main/css/main.css")
remote_file = ["/home/ubuntu/sait/main/static/main/css/main.css", "/home/ubuntu/sait/staticfiles/main/css/main.css"]

# ==== СОЕДИНЕНИЕ SSH ====
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port=port, username=username, password=password)

# ==== SFTP ЗАЛИВКА ФАЙЛА ====
for file in remote_file:
    sftp = ssh.open_sftp()
    sftp.put(str(local_file), file)
    sftp.close()


local_file = Path("sait/main/templates/main/")
sftp = ssh.open_sftp()

for item in local_file.iterdir():
    remote_item = f"/home/ubuntu/sait/main/templates/main/{item.name}"
    sftp.put(str(item), remote_item)

local_file = Path("sait/main/templates/registration/")
sftp = ssh.open_sftp()

for item in local_file.iterdir():
    remote_item = f"/home/ubuntu/sait/main/templates/registration/{item.name}"
    sftp.put(str(item), remote_item)

# ==== ПЕРЕЗАПУСК СЕРВИСА (Gunicorn) ====
stdin, stdout, stderr = ssh.exec_command("sudo systemctl restart myproject_gunicorn")
print(stdout.read().decode())
print(stderr.read().decode())

ssh.close()
print("Файл загружен и сервис перезапущен ✅")