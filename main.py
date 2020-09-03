# -*- coding: utf-8 -*-

import sys
import re
from datetime import datetime
from pprint import pprint

def help():
    print('Please Provide txt filename in cmd args')

# returns tuple of (time, user, id, name)
# returns None if error (cannot parse line)
def parse_line(line):
    # split before and after '시작' 
    try:
        start_index = line.index('시작')
    except:
        return None

    # extract time string
    time_str = line[:start_index].strip()
    chat_str = line[start_index:].strip()

    # extract username and chat content
    try:
        colon_index = chat_str.index(':')
    except:
        return None
    user_str = chat_str[4:colon_index].strip()
    check_str = chat_str[colon_index+2:]

    # extract student id and name
    check_token = check_str.split(' ', 1)
    try:
        id_str = check_token[0]
        name_str = check_token[1]
        # check if id_str matched general format of student id
        if not re.fullmatch('[\d]{8}', id_str):
            raise Exception('Id Str not matched')
        # package strings into tuple and return
        return (time_str, user_str, id_str, name_str)
    except:
        return None

### helper functions for comparing timestring
def is_str_before_1310(timestr):
    parsed_time = datetime.strptime(timestr, "%H:%M:%S").time()
    compare_time = datetime.strptime("13:10:00", "%H:%M:%S").time()
    return parsed_time < compare_time

def is_str_after_1400(timestr):
    parsed_time = datetime.strptime(timestr, "%H:%M:%S").time()
    compare_time = datetime.strptime("14:00:00", "%H:%M:%S").time()
    return parsed_time > compare_time
    
def parse(filename):
    f = open(filename)
    # check_db: dictionary
    # key : student id
    # value : [name, username, username]
    # name corresponds to actual name
    # first username corresponds to check before 13:10
    # second username coresponsd to check after 14:00
    # if no check in that time, stores None value
    check_db = dict()
    error_lines = []

    # line by in in file
    for line in f:
        # try parse the line
        result = parse_line(line.strip())
        # get time, username, id, name from line
        try:
            # raise error if could not parse the line
            if result == None:
                raise Exception("Cannot parse")
            time, user, id, name = result
            before_1310 = is_str_before_1310(time)
            after_1400 = is_str_after_1400(time)
            # raise error if time is not before 13:10 or after 14:00
            if (not before_1310 and not after_1400):
                raise Exception("Time invalid")

            # if both before 13:10 and after 14:00, something went wrong!
            if before_1310 and after_1400:
                raise Exception("TENET")
            
            # So here, only one of before 13:10 or after 14:000
            # Put appropriate data in check_db
            # id not in dict yet, so need to put it
            if id not in check_db.keys():
                check_db[id] = [name, None, None]
            # before 13:10 case
            if before_1310:
                check_db[id][1] = user
            # after 14:00 case
            if after_1400:
                check_db[id][2] = user
            #print(time, before_1310, after_1400, "id", id, "name", name)
            
        # Error case
        except:
            error_lines.append(line)
            #print("Error parsing line: ---" + line.strip() + "---")
        # End of for loop
    # return the parsed check_db and error_lines
    return (check_db, error_lines)

def output_check_csv(check_db, filename):
    f = open(filename, 'w')
    f.write('Student ID, Name, Valid, Checked before 13:10, Checked before 14:00, User name 1, User name 2\n')
    # key of dict is student id
    # value of dict is [name, username before 13:10, username after 14:00]
    for id, data in check_db.items():
        name = data[0]
        fst_username = data[1]
        snd_username = data[2]
        fst_check = (fst_username != None)
        snd_check = (fst_username != None)
        valid_bool = fst_check and snd_check and (fst_username == snd_username)
        valid_check = 'X'
        if valid_bool:
            valid_check = 'O'
        f.write("{}, {}, {}, {}, {}, {}, {}\n".format(id, name, valid_check, fst_check, snd_check, fst_username, snd_username))
    f.close()


def output_error_csv(error_lines, filename):
    f = open(filename, 'w')
    for index, line in enumerate(error_lines):
        f.write("{}, {}\n".format(index, line.strip()))

if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)
    if argc <= 1:
        help()
    else:
        input_filename = argv[1]
        check_db, error_lines = parse(input_filename)

        output_filename = "output/check_output.csv"
        output_check_csv(check_db, output_filename)

        error_filename = "output/error_output.csv"
        output_error_csv(error_lines, error_filename)
        #pprint(check_db)
        #print("============================")
        #pprint(error_lines)