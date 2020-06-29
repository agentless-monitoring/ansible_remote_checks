#!/usr/bin/python2

import time
import subprocess
from ansible.module_utils.basic import AnsibleModule
import io

def get_proc_stat():
  f = open("/proc/stat", "r")
  l = f.readline().split()[1:5]
  f.close()
  for i in range(len(l)):
    l[i] = int(l[i])
  return l

def get_top_most_cpu_procs():
  cmd=["ps","-hax","-k","-%cpu","-o","comm %cpu pid args"]
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  output, error = process.communicate()

  return output.splitlines()


def get_cpu_usage():
  a = get_proc_stat()
  time.sleep(0.25)
  b = get_proc_stat()
  for i in range(len(a)):
    b[i] = b[i]- a[i]
  t = 100.0 / sum(b)
  
  processes = get_top_most_cpu_procs()[:10]
  
  
  return {
    "user": int(round(b[0] * t, 0)),
    "nice": int(round(b[1] * t, 0)),
    "sys":  int(round(b[2] * t, 0)),
    "idle": int(round(b[3] * t, 0)),
    "used": int(round(100.0 - b[3] * t, 0)),
    "processes": processes
  }

def main():
  module_args= dict()

  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True
  )

  cpu_used = get_cpu_usage()

  try:
    result = dict(cpu_used = cpu_used)
  except Exception as ex:
    module.fail_json(msg=str(ex))

  module.exit_json(**result)

if __name__ == '__main__':
  main()

