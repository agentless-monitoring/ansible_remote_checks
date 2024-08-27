#!/usr/bin/python

import os
import subprocess
from ansible.module_utils.basic import AnsibleModule
import json

def get_service_info(servicename, module):
  ret={}
  values={}
 
  if servicename:
    cmd = "systemctl status %s --no-pager" % (servicename)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
     
    active = output.splitlines()[2]
    active_status = active.split()[1]
 
    values['message'] = active_status,
    values['status'] = process.returncode          
    ret[servicename]= values

  else:
    cmd = "systemctl list-units --no-legend --state=failed -o json"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    # 91 == '[' -> This is a json output
    if output != b'' and output[0] == 91:
      failed_json_out = json.loads(output)
      for json_status in failed_json_out:
        servicename = json_status['unit']
        values['message'] = json_status["description"]
        values['status'] = 3
        ret[servicename]= values
    # RHEL8 systems silently ignore "-o json" parse "human status" instead
    else:
      for line in output.splitlines():
        value = line.split()
        servicename = value[0]
        values['message'] = value[2],
        values['status'] = 3
        ret[servicename]= values
  return ret

def main():

  args = dict(servname=dict(type='str'))
  
  module = AnsibleModule(
    argument_spec = args,
    supports_check_mode = True
  )

  servicename = module.params['servname']

  try:
    result = dict(serviceinfo = get_service_info(servicename, module))
  except Exception as ex:
    module.fail_json(msg=str(ex))

  module.exit_json(**result) 

if __name__ == '__main__':
  main()

