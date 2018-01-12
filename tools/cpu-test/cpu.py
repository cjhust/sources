#!/usr/bin/python


import os
import sys
import re
import termcolor


def INFO(buf):
  print termcolor.colored(buf, "grey")
  
  
def ERROR(buf):
  print termcolor.colored(buf, "red")
  
   
def SHOW(buf):
  print termcolor.colored(buf, "green")


def get_cpu_name(result):
  cmd = 'cat /proc/cpuinfo |grep "model name"|uniq|cut -d: -f 2'
  fd = os.popen(cmd)
  data = fd.readline()
  fd.close() 
  data = re.sub(" +", " ", data)
  data = data.strip() 
  result["cpu_name"] = data
      

def get_physical_cpu_num(result):
  cmd = 'cat /proc/cpuinfo |grep "physical id" |sort |uniq -c |wc -l'
  fd = os.popen(cmd)
  data = fd.readline()
  fd.close()  
  result["physical_cpu_num"] = int(data)


def get_physical_cpu_cores(result):
  cmd = 'cat /proc/cpuinfo | grep "cpu cores" | uniq |cut -d: -f 2'
  fd = os.popen(cmd)
  data = fd.readline()
  fd.close() 
  result["physical_cpu_cores"] = int(data)   
  
   
def get_logic_cpu_cores(result):
  cmd = 'cat /proc/cpuinfo | grep "siblings" | uniq |cut -d: -f 2'
  fd = os.popen(cmd)
  data = fd.readline()
  fd.close() 
  result["logic_cpu_cores"] = int(data)
 
      
def get_logic_cpu_num(result):
  cmd = 'cat /proc/cpuinfo |grep "processor" |wc -l'
  fd = os.popen(cmd)
  data = fd.readline()
  fd.close() 
  result["logic_cpu_num"] = int(data)


def turn_on_hyperthread(result):
  if (result["logic_cpu_cores"] == result["physical_cpu_cores"]):
    result["hyperthread"] = "no"
  else:
    result["hyperthread"] = "yes"  


def print_cpu_info(result):
  header = "------------------" + "cpu information" + "------------------"
  SHOW(header)
  
  num = 0
  for item in sorted(result):
    num += 1
    info = "(%d): %s = %s"   %(num, item, result[item])
    INFO(info)
  
  
def ls_cpu_info():
  result = {}
  get_cpu_name(result)
  get_physical_cpu_num(result)
  get_physical_cpu_cores(result)
  get_logic_cpu_cores(result)
  get_logic_cpu_num(result)
  turn_on_hyperthread(result)
  print_cpu_info(result)


if __name__ == "__main__":
  ls_cpu_info()
  
  
  
