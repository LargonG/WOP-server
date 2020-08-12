import pymysql
import os
import time

while True:
    #такие костыли с папкой нужны с целью того, что
    #если реализовывать эту штуку через один файл
    #он может не открыться потому что тестирующая система в него что то записывает
    #поэтому тестирующая система еще должна создавать файлы в директории outmanager

    dirlist = os.listdir("outmanager")
    for line in dirlist:
        problem_id, submit_id = line.split("_")
        print("problem_id =", problem_id)
        print("submit_id =", submit_id)
        #проверяем на ошибку компиляции
        if os.path.exists(f"submits/{problem_id}/{submit_id}/compilation.txt"):
            #послать репорт, что произошла ошибка компиляции
            continue
        with open(f"tests/{problem_id}/problem.cfg", 'r') as cfg:
            for line1 in cfg:
                param, value = line1.split(":")
                while value[0] == ' ':
                    value = value[1:]
                if param == "test_sets":
                    test_sets = int(value)
        cfg.close()

        print("test_sets =", test_sets)
        last_test = 1
        while os.path.exists(f"submits/{problem_id}/{submit_id}/report{last_test}.txt"):
            last_test += 1
        last_test -= 1
        print("last_test =", last_test)
        
        with open(f"submits/{problem_id}/{submit_id}/report{last_test}.txt") as rep:
            report = rep.read()
            if report == "OK" and last_test == test_sets:
                print("OK") #отладочный вывод
                #здесь надо послать репорт о том что задача на ОК
                
            else:
                print(report, last_test) #отладочный вывод
                #здесь послать репорт в формате <ошибка><номер_теста>
                
        rep.close()
        os.remove(f"outmanager/{line}")
    time.sleep(.2) #это нужно чтобы несильно засорялся процессор
