import os
from string import Template
import xml.etree.ElementTree as ET

class RunbookStepSuccessResponse:
    def __init__(self):
        self.succeeded = True
        
class RunbookStepFailedResponse:
    def __init__(self, template_variables):
        self.succeeded = False
        self.template_variables = template_variables        

def get_component_conf_dir(host_path, service, component):
  bundle_dir_template = Template("$service/components/$component/DEFAULT/conf")
  for path in os.walk(host_path):
    if (path[0].endswith(bundle_dir_template.substitute(service=service,component=component))):
        return path[0]

def host_has_component(host_path, service, component):
  return (not get_component_conf_dir(host_path, service, component) is None)

def get_property_value(host_path, service, component, file, property):
  conf_dir = get_component_conf_dir(host_path, service, component)
  tree = ET.parse(conf_dir + "/"+ file)
  root = tree.getroot()
  for elem in root.iterfind('property'):
    for inner_elem in elem.iterfind('name'):
      if inner_elem.text == property:
        for value in elem.iterfind('value'):
          return value.text
          
def get_file(host_path, relative_path):
  return open(host_path + "/" + relative_path, 'r')