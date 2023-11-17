#!/usr/bin/python

import os
import subprocess
from ansible.module_utils.basic import AnsibleModule

def get_subscription_info(module):
  
  cmd = ["sudo", "-A","subscription-manager", "status"]
  
  sudo_env = os.environ.copy()
  sudo_env["SUDO_ASKPASS"]="/bin/false"
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=sudo_env)
  output, error = process.communicate()

  # Python3 reads the output as byte and needs decoding
  try:
    output = output.decode()
  except (UnicodeDecodeError, AttributeError):
    pass

  return_code = process.returncode

  return {'output': output, 'return_code': return_code }

def main():
  
  module = AnsibleModule(
    argument_spec = dict(),
    supports_check_mode = True
  )
  
  try:
    result = dict(subscription = get_subscription_info(module))
  except Exception as ex:
    module.fail_json(msg=str(ex))
 
  module.exit_json(**result) 

if __name__ == '__main__':
  main()
