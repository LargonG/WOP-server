import pymysql
import os
import time
import shutil
from contextlib import closing
from pymysql.cursors import DictCursor

while True:
    #такие костыли с папкой нужны с целью того, что
    #если реализовывать эту штуку через один файл
    #он может не открыться потому что тестирующая система в него что то записывает
    #поэтому тестирующая система еще должна создавать файлы в директории outmanager

    dirlist = os.listdir("outmanager")
    for line in dirlist:
        problem_id, submit_id = line.split("_")
        maxtime = 0
        maxmem = 0
        print(problem_id, submit_id)
        #проверяем на ошибку компиляции
        if os.path.exists(f"submits/{problem_id}/{submit_id}/compilation.txt"):
            #послать репорт, что произошла ошибка компиляции
            try:
                with closing(pymysql.connect(host="localhost", user="root", password="", db="WOP", charset="utf8mb4", cursorclass=DictCursor)) as connection:
                    connection.cursor().execute(f"UPDATE submits{problem_id} SET status = \"CE\" WHERE id = {submit_id}")
                    connection.commit()
                print("compilation error")
            except:
                continue
            os.remove(f"outmanager/{line}")
            continue

        if os.path.exists(f"submits/{problem_id}/{submit_id}/maxtime.txt"):
            with open(f"submits/{problem_id}/{submit_id}/maxtime.txt") as timefile:
                maxtime = int(timefile.read())
            timefile.close()
        else:
            maxtime = 0

        if os.path.exists(f"submits/{problem_id}/{submit_id}/maxmem.txt"):
            with open(f"submits/{problem_id}/{submit_id}/maxmem.txt") as memfile:
                maxmem = int(memfile.read())
            memfile.close()
        else:
            maxmem = 0

        with open(f"tests/{problem_id}/problem.cfg", 'r') as cfg:
            for line1 in cfg:
                param, value = line1.split(":")
                while value[0] == ' ':
                    value = value[1:]
                if param == "test_sets":
                    test_sets = int(value)
        cfg.close()

        last_test = 1
        while os.path.exists(f"submits/{problem_id}/{submit_id}/report{last_test}.txt"):
            last_test += 1
        last_test -= 1
        
        with open(f"submits/{problem_id}/{submit_id}/report{last_test}.txt") as rep:
            report = rep.read()
            if report == "OK" and last_test == test_sets:
                #здесь надо послать репорт о том что задача на ОК
                try:
                    with closing(pymysql.connect(host="localhost", user="root", password="", db="WOP", charset="utf8mb4", cursorclass=DictCursor)) as connection:
                        connection.cursor().execute(f"UPDATE submits{problem_id} SET status = \"OK\" WHERE id = {submit_id}")
                        connection.cursor().execute(f"UPDATE submits{problem_id} SET maxtime = {maxtime} WHERE id = {submit_id}")
                        connection.cursor().execute(f"UPDATE submits{problem_id} SET maxmem = {maxmem} WHERE id = {submit_id}")
                        connection.commit()
                    print("OK")
                except:
                    continue
                
            else:
                #здесь послать репорт в формате <ошибка><номер_теста>
                try:
                    with closing(pymysql.connect(host="localhost", user="root", password="", db="WOP", charset="utf8mb4", cursorclass=DictCursor)) as connection:
                        connection.cursor().execute(f"UPDATE submits{problem_id} SET status = \"{report} {last_test}\" WHERE id = {submit_id}")
                        connection.cursor().execute(f"UPDATE submits{problem_id} SET maxtime = {maxtime} WHERE id = {submit_id}")
                        connection.cursor().execute(f"UPDATE submits{problem_id} SET maxmem = {maxmem} WHERE id = {submit_id}")
                        connection.commit()
                    print(report, last_test)
                except:
                    continue
                
        rep.close()
        os.remove(f"outmanager/{line}")
        shutil.rmtree(f"submits/{problem_id}/{submit_id}", ignore_errors=True)
    time.sleep(.05)
