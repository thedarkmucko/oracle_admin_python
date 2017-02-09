import os
import itertools
import sys
from pwd import getpwnam
from collections import deque
 
help = """
Simple Oracle Administrator
 
Parameters:
-c         : use for creating
-r         : use for removing
--help     : print this help
 
Options:
standard        : defines /products/oracle directory structure
default         : defines the OFA directory structure
"""
 
def check_path(v_input):
    if os.path.isdir(v_input):
        return True
    else:
        return False
 
def create_it(list):
        if not list:
                print("Structure is already in place")
        else:
                for i in list:
                        os.mkdir(i,0755)
                        uid = getpwnam('oracle').pw_uid
                        gid = getpwnam('oracle').pw_gid
                        os.lchown(i,uid,gid)
                        print("Directory created: " + i)
 
def create_oracle_structure(v_version):
    if v_version == "default":
        data = list(itertools.ifilterfalse(check_path, ['/u01', '/u01/app', '/u01/app/oracle']))
        create_it(data)
    elif v_version == "standard":
        data = list(itertools.ifilterfalse(check_path, ['/products', '/products/oracle']))
        create_it(data)
    else:
        print "Nothing to do with parameter: " + v_version
 
def remove_it(list):
        if not list:
                print("Nothing to remove")
        else:
                for entry in reversed(list):
                       os.rmdir(entry)
                       print("Removed "+entry)
 
def delete_oracle_structure(v_version):
        if v_version == "default":
                try:
                        data = list(itertools.ifilter(check_path, ['/u01', '/u01/app', '/u01/app/oracle']))
                        remove_it(data)
                except OSError:
                    print("removing failed")
        elif v_version == "standard":
                try:
                        data = list(itertools.ifilterfalse(check_path, ['/products', '/products/oracle']))
                        remove_it(data)
                except OSError:
                    print("removing failed")
 
def check_valid_option(parameter):
        return {
                '-c': True,
                '-r': True,
                '--help': True,
                'standard': True,
                'default': True }.get(parameter, False)
 
 
def execute_parameters(count,parameters):
        items = deque(parameters)
 
    try:
            pop_count = 0
            while (pop_count != count):
                    if (count > 1):
                            parameter = items.popleft()
                            pop_count = pop_count + 1
                            value     = items.popleft()
                            pop_count = pop_count + 1
                            if parameter == "-c" and (value == "default" or value == "standard"):
                                    create_oracle_structure(value)
                            if parameter == "-r" and (value == "default" or value == "standard"):
                                    delete_oracle_structure(value)
                    elif (count == 1):
                            parameter = items.popleft()
                            pop_count = pop_count + 1
                            if parameter == "--help":
                                    print help
    except IndexError:
            print("OutOffBounds Error")
 
def main(my_args=None):
        cmdargs = sys.argv[1:]
        total = len(sys.argv)-1
 
    if total < 1:
            print "Not enough parameters"
 
    for i in list(cmdargs):
            input = str(i)
            data = check_valid_option(i)
            if data == False:
                    print "Invalid option added... Quit"
                    sys.exit(-1)
    execute_parameters(total,cmdargs)
 
 
if __name__== '__main__':
    main()
