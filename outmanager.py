import pymysql
import os
import time

mysql_con = pymysql.connect('localhost', 'root', '', 'WOP')

while True:
    #такие костыли с папкой нужны с целью того, что
    #если реализовывать эту штуку через один файл
    #он может не открыться потому что тестирующая система в него что то записывает
    #поэтому тестирующая система еще должна создавать файлы в директории outmanager

    dirlist = os.listdir("outmanager")
    for line in dirlist:
        problem_id, submit_id = line.split("_")
        #проверяем на ошибку компиляции
        if os.path.exists(f"submits/{problem_id}/{submit_id}/compilation.txt"):
            #послать репорт, что произошла ошибка компиляции
            with mysql_con:
                cur = mysql_con.cursor()
                try:
                    cur.execute(f"UPDATE submits{problem_id} SET status = \"CE\" WHERE id = {submit_id}")
                except:
                    continue
            os.remove(f"outmanager/{line}")
            continue
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
                with mysql_con:
                    cur = mysql_con.cursor()
                    try:
                        cur.execute(f"UPDATE submits{problem_id} SET status = \"OK\" WHERE id = {submit_id}")
                    except:
                        continue
                
            else:
                #здесь послать репорт в формате <ошибка><номер_теста>
                with mysql_con:
                    cur = mysql_con.cursor()
                    try:
                        cur.execute(f"UPDATE submits{problem_id} SET status = \"{report} {last_test}\" WHERE id = {submit_id}")
                    except:
                        continue
                
        rep.close()
        os.remove(f"outmanager/{line}")
    time.sleep(.05)
