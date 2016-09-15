from runbook import *

def main():
  java_version_file = get_file(host_path, "os/reports/java_version.txt")
  java_version_output = java_version_file.read()
  java_version_file.close()
  
  java_version = java_version_output.split('\n')[0].split(' ')[2].replace('"','')
  major_version = int(java_version.split('.')[1])
  update_version = int(java_version.split('.')[2].split('_')[1])
  if (major_version == 8 and update_version < 61):
    return RunbookStepFailedResponse({'java_version':java_version})
  return RunbookStepSuccessResponse()
  
result = main()