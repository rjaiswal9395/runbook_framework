import re
from datetime import datetime
from datetime import timedelta
import sys
import os

def logFileEndTimeDetector(filepath):
    with open(filepath, 'r') as file_to_check:
        for line in reversed(list(file_to_check)):
            match = re.search(r'(^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            if match:
                end_time = datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S')
                start_time = end_time -timedelta(days = 1)
                break

    return start_time



def keyword_extractor(filepath,writepath,start_time,string):
  error_list=[]

  try:
    filevariable=open(filepath, "r")
  except Exception as error:
    print(error)
    return -1
  filevariable.seek(0);
  count=0
  file_lines = filevariable.readlines()
  for line in reversed(file_lines):
      time = re.search('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
      if time:
        currentTime = datetime.strptime(time.group(),'%Y-%m-%d %H:%M:%S')
        if currentTime <=start_time:
          break
      if "STARTUP_MSG" in line:
        break
      error = re.findall(string, line)
      if error:
        # dir = re.search("/(.*)", line)
        count += 1
        error_list.append(line)
        # if dir:
        #     f.write("TIME: "+ str(currentTime) + " Directory Name " + dir.group(0).replace(":", "") + " ERROR TYPE " +file_lines[(file_lines.index(line))+1] )
  with open(writepath, "a") as f:
    if (error_list):
      for element in error_list:
        f.write(element)
  return(count)

def maincheck(read_path, write_path,string):
  try:
    start_time=logFileEndTimeDetector(read_path)
    s= (keyword_extractor(read_path, write_path,start_time,string))
    return (s)
  except Exception as error:
    print("File too large exception.")
    return -1

if __name__ == '__main__':
	start_time=logFileEndTimeDetector(os.environ["Log_File_Location"])
	exit(keyword_extractor(os.environ["Log_File_Location"],os.environ["Final Write Location"],start_time,"timeout while waiting for channel to be ready"))