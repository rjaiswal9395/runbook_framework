#!/usr/bin/python
import os
import sys
import yaml
import argparse
import subprocess
import tarfile
import shutil
from jinja2 import Template

class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colored_print(message, color):
    print color + message + tcolors.ENDC

def get_step(steps, step_number):
    for step in steps:
        if (step_number == 'CASE'):
            colored_print("Case needs to be created!", tcolors.FAIL)
            exit(1)
        if (step_number == 'END'):
            colored_print("Runbook finished", tcolors.HEADER)
            exit(0)
        if (step['step'] == step_number):
            return step

def step_ok(steps, step):
    colored_print("Ok: " + step['name'], tcolors.OKGREEN)
    #execute_step(steps,get_step(steps, step['on_success']), host_tar_paths)
    
def step_failed(steps, step):
    colored_print("Failed: " + step['name'], tcolors.FAIL)
    try:
        with file(script_dir + "/scripts/" + step['step_failure_template']) as f:
            source = f.read().decode('utf-8')
            template = Template(source)
            colored_print(template.render(), tcolors.HEADER)
    except KeyError:
        print "No template available for this exception"
    execute_step(steps,get_step(steps, step['on_failure']))
    
def execute_step(steps, step):
	response = subprocess.call("python" +" "+ script_dir + "/scripts/" + step['script'], shell=True)
	print response
	if (response>=1):       
		step_failed(steps, step)
	
	step_ok(steps,step)

def host_tars(members):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ".tgz":
            yield tarinfo

def extract_bundle(bundle, output_dir):
    host_tar_paths = []
    bundle_id = os.path.basename(bundle).split('.')[0]
    bundle_base_path = output_dir + "/" + bundle_id
    if (not os.path.isdir(bundle_base_path)):
      tar = tarfile.open(bundle)
      for tar_file in host_tars(tar):
        tar_basename = os.path.basename(tar_file.name)
        tar_file.name = bundle_id + "/" + tar_basename
        tar.extract(tar_file, path=output_dir)
        sub_tar = tarfile.open(bundle_base_path + "/" + tar_basename)
        sub_tar.extractall(path=output_dir + bundle_id)
        host_tar_paths.append(bundle_base_path + "/" + tar_basename.replace('.tgz',''))
        sys.stdout.write('.')
        sys.stdout.flush()
        sub_tar.close
      print '.\n'
      tar.close
    else:
      for path in os.listdir(bundle_base_path):
        host_path = bundle_base_path + "/" + path
        if os.path.isdir(host_path):
          host_tar_paths.append(host_path)
    return host_tar_paths

def execute_runbook(runbook_file, script_dir):
    steps = yaml.load(open(runbook_file).read())
    colored_print("Running runbook from " + runbook_file + "\n", tcolors.BOLD)
    #colored_print("Extracting Bundle " + os.path.basename(bundle) + " to " + output_dir + "\n", tcolors.BOLD)
    #host_tar_paths = extract_bundle(bundle, output_dir)
    print "Service: " + steps['service']
    print "Name: " + steps['name']
    print "Description: " + steps['description']
    print "-------------------------------\n"
    for step in steps['steps']:
        execute_step(steps['steps'],step)


os.environ["Log_File_Location"] = "/Users/rjaiswal/Desktop/SmartSenseScripts 2/HDFS/temp.txt"
os.environ["Final Write Location"]= "/Users/rjaiswal/Desktop/SmartSenseScripts 2/HDFS/new.txt"      
parser = argparse.ArgumentParser(description='Execute a specific Hortonworks Support Runbook')
parser.add_argument('-f','--file', help="The path to the runbook's yaml file",required=True)
#parser.add_argument('-b','--bundle', help="The path to the unencrypted bundle (.tgz)",required=True)
#parser.add_argument('-o','--output', help="The path to decompress the bundle into",required=True)
args = parser.parse_args()
script_dir = os.path.dirname(args.file)
#bundle = args.bundle
#output_dir = args.output
execute_runbook(args.file, script_dir)