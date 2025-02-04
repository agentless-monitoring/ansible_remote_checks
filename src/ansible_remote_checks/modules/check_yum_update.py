#!/usr/bin/python

import os
import subprocess
import re
from ansible.module_utils.basic import AnsibleModule

def get_update_info(module):
  
  cmd = ["sudo", "-A","yum", "check-update"]
  
  sudo_env = os.environ.copy()
  sudo_env["SUDO_ASKPASS"]="/bin/false"
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=sudo_env)
  output, error = process.communicate()

  # Python3 reads the output as byte and needs decoding
  try:
    output = output.decode()
  except (UnicodeDecodeError, AttributeError):
    pass


  updates = {}
  return_code = process.returncode

  if (return_code == 1):
    module.fail_json(msg='sudo/yum check-update failed. stdout: %s stderr: %s' % (output, error))

  elif return_code == 100:
    updates["status"] = 100
    first_match = False
    update_count = 0
      
    #line should have three parts (name, version, channel)
    package_regex = "^([^\s]+)\s+([^\s]+)\s+([^\s]+)\s*$"
    
    for idx, line in enumerate(output.splitlines()):
      package = re.match(package_regex, line)
      if package:
        first_match = True
        update_count += 1
        updates[update_count] = package.groups()
      elif first_match:
        module.fail_json(msg='Cannot parse package in output! stdout: %s stderr: %s' % (output, error))

    return updates

  elif return_code == 0:
    updates["status"] = 0
    return updates

def main():
  
  module = AnsibleModule(
    argument_spec = dict(),
    supports_check_mode = True
  )
  
  try:
    result = dict(updateinfo = get_update_info(module))
  except Exception as ex:
    module.fail_json(msg=str(ex))
 
  module.exit_json(**result) 

if __name__ == '__main__':
    main()
