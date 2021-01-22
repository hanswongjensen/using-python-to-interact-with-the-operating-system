#!/usr/bin/env python3

import os
import re
import csv
import sys
import operator

def error_csv():
  with open("syslog.log", 'r') as filename:
    error_list = []
    error_dict = {}
    for line in filename:
      regex_error = re.search(r'(ERROR [\w\' \[]*) ', line)
      if regex_error is not None:
        error_list.append(regex_error)

    for error in error_list:
      error_clean = error.group(0).replace("ERROR ", "").strip()
      if error_clean in error_dict:
        error_dict[error_clean] += 1
      else:
        error_dict[error_clean] = 1

    error_dict_sort = sorted(error_dict.items(), key=operator.itemgetter(1), reverse=True)

    with open("error_message.csv", 'w', newline = "") as output:
      fieldnames = ["Error", "Count"]
      csvwrite = csv.DictWriter(output, fieldnames = fieldnames)
      csvwrite.writeheader()

      for i in error_dict_sort:
        csvwrite.writerow({"Error": i[0], "Count": i[1]})


def users_csv():
        with open("syslog.log", 'r') as filename:
                users_dict = {}
                users_dict_sort = {}
                for line in filename:
                        regex_user = re.search(r'\(.*?\)', line)
                        regex_user_error = re.search(r'ERROR ', line)
                        regex_user_clean  = regex_user.group(0).strip("()")
                        if regex_user_clean in users_dict:
                                if regex_user_error is not None:
                                        users_dict[regex_user_clean][1] += 1
                                else:
                                        users_dict[regex_user_clean][0] += 1
                        else:
                                if regex_user_error is not None:
                                        users_dict[regex_user_clean] = [0,1]
                                else:
                                        users_dict[regex_user_clean] = [1,0]
        users_dict_sort = sorted(users_dict.items(), key = operator.itemgetter(0))

        with open("user_statistics.csv", 'w', newline = "") as output:
                fieldnames = ["Username", "INFO", "ERROR"]
                csvwrite = csv.DictWriter(output, fieldnames = fieldnames)
                csvwrite.writeheader()
                
                for i in users_dict_sort:
                        info_num = i[1][0]
                        error_num = i[1][1]
                        csvwrite.writerow({"Username": i[0], "INFO": info_num, “ERROR”: error_num})

error_csv()
users_csv()
