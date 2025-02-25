#!/usr/bin/python

import os
import subprocess
import re
from ansible.module_utils.basic import AnsibleModule

# multiline handling 
# if a package name exceeds 25 chars
# and the rest of the line does not contain alpha numerical chars 
# there will be a line break
def is_multiline(line):
  if len(line) >= 25 and not any(char.isalpha() for char in line[25:]):
    return True
  else:
    return False

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
    skip_next = False
    obsoleting_packages = False

    splitted = output.splitlines()
    for idx, line in enumerate(splitted):
      if skip_next:
        # skip multiple time for multi lines  
        if not is_multiline(line):  
          skip_next = False
          
        continue
      
      if is_multiline(line):
        if idx < len(line) - 1:
          next_line = splitted[idx + 1]
          line = f"{line} {next_line}"
          skip_next = True
     
      # specials like obsoleting packages and security info 
      if line.startswith("Obsoleting Packages"):
        obsoleting_packages = True   
        continue
      if obsoleting_packages:
        skip_next = True 
      if line.startswith("Security:"):
        continue
     
      package = re.match(package_regex, line)
      if package:
        first_match = True
        update_count += 1
        updates[update_count] = package.groups()
      elif first_match:
        module.fail_json(msg='Cannot parse package in output! Line: %s, stdout: %s, stderr: %s' % (line, output, error))

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
