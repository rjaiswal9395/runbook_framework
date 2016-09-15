from runbook import *

def main():
  if (host_has_component(host_path, 'HDFS', 'DataNode')):
    auth_to_local_rules = get_property_value(host_path, 'HDFS', 'DataNode','core-site.xml','hadoop.security.auth_to_local')
    if "DEFAULT" not in auth_to_local_rules:
      return RunbookStepFailedResponse({'auth_to_local_rules':auth_to_local_rules})
  return RunbookStepSuccessResponse()

result = main()