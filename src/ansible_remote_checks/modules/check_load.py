#!/usr/bin/python

import os 
from ansible.module_utils.basic import AnsibleModule


def get_load():
  ret={}
  with open('/proc/loadavg', 'r') as loadavg:
    for line in [l.split() for l in loadavg.readlines()]:
      values = line
      ret['1min'] = values[0]
      ret['5min'] = values[1]
      ret['15min'] = values[2]
      ret['scheduling_entities'] = values[3]
      ret['pid'] = values[4]

  #cmd = "grep -i 'physical id' /proc/cpuinfo" #| sort -u | wc -l "
  #cmd = "cat /proc/cpuinfo"
  #process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
  #output, error = process.communicate()
  ret['cpu_cores'] = os.sysconf('SC_NPROCESSORS_ONLN')
  return ret
  
def main():
  module_args= dict()

  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True
  )

  loadinfo = get_load()

  try:
    result = dict(loadinfo=loadinfo)
  except Exception as ex:
    module.fail_json(msg=str(ex))
 
  module.exit_json(**result)

if __name__ == '__main__':
  main()

