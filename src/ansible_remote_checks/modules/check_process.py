#!/usr/bin/python2

import re
import subprocess
from ansible.module_utils.basic import AnsibleModule

def get_procs(process_regex, cmdline_regex):
  cmd=["ps","-hax","-o","comm pid args"]
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  output, error = process.communicate()
  lines = output.splitlines()
  processes = []

  for line in lines:
    process = line.split()[0]
    cmdline = ' '.join(line.split()[2:])

    if (not process_regex or re.findall(process_regex, process)) and (not cmdline_regex or re.findall(cmdline_regex, cmdline)):
      processes.append(line)

  return {
    "processes": processes
  }

def main():
  module_args= dict(
    process = dict(type='str', required=True),  
    cmdline = dict(type='str')
  )

  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True
  )

  process_regex = module.params['process']
  cmdline_regex = module.params['cmdline']
  procs = get_procs(process_regex, cmdline_regex)

  try:
    result = dict(procs = procs)
  except Exception as ex:
    module.fail_json(msg=str(ex))
  
  module.exit_json(**result)

if __name__ == '__main__':
  main()
