import socket
import os

SERVER_IP = "192.168.50.19"
PORT = 1337
BUF_SIZE = 2*1024
 
sock = socket.socket()
sock.bind((SERVER_IP, PORT))

while True:
    sock.listen(1)
    con, addr = sock.accept()
    print(f"Connection with {addr}")
    sub = str(con.recv(BUF_SIZE).decode('utf-8'))
    sub.replace('\r', '')
    code_list = sub.split("\n")

    lang = code_list[0].split(":")[1]
    task_id = code_list[1].split(":")[1]
    submit_id = code_list[2].split(":")[1]

    sub = ''
    for i in code_list[3:]:
        sub += i

    if sub:
        if not os.path.exists("submits"):
            os.mkdir("submits")
        if not os.path.exists(f"submits/{task_id}"):
            os.mkdir(f"submits/{task_id}")
        os.mkdir(f"submits/{task_id}/{submit_id}")
        with open(f"submits/{task_id}/{submit_id}/main.{lang}", 'w') as file:
            file.write(sub)
        file.close()
        con.send(bytes("accepted", encoding='utf-8'))
        con.close()
        
        #запустить тестирующий скрипт
        with open("testengine.cfg", 'w') as file:
            file.write(f"task_id: {task_id}\nsubmit_id: {submit_id}\nlang: {lang}")
        file.close()
        os.system("testengine.exe >logs.txt")
    con.close()
    
