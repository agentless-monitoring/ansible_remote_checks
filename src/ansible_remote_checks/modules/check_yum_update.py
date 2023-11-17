#!/usr/bin/python

import os
import subprocess
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

  lines = output.splitlines()
  return_code = process.returncode

  if (return_code == 1):
    module.fail_json(msg='sudo/yum check-update failed. stdout: %s stderr: %s' % (output, error))
  
  updates = {}
  grouped_updates = {}
  newLines = 0
  update_count = 0
  skipLines = 0
  obsoleting_packages = False

  for idx,line in enumerate(lines):

    lineindex = idx

    if line.strip() == 'Obsoleting Packages':
      obsoleting_packages = True
      skipLines = skipLines + 1 

    #start after first blank line
    if newLines == 1:
      #line was already appended to the previous line or is the first line from obsoleting packages
      if skipLines > 0:
        skipLines -= 1
        continue
      
      if not len(lines) > lineindex:
        break
      
      #line should have three parts (name, version, channel)
      update = lines[lineindex].split()
 
      #if less than three parts take the next line and append
      lineindex = idx + 1

      while len(update) < 3:
        for entry in lines[lineindex].split():
          update.append(entry)

        skipLines +=1
        lineindex +=1
      
      update_count += 1
      updates[update_count]= update
      
    #obsoleting packages are currently not handled, therefore the module will return all results and stop
    if obsoleting_packages:
      return updates

    if line.strip() == '':
      newLines += 1
      continue

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
