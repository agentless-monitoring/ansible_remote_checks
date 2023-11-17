#!/usr/bin/python

import os
import subprocess
import re
from ansible.module_utils.basic import AnsibleModule

def get_memory_info(memory=False, swap=False, max_number_processes=10):
 
  ret = {}
  meminfo = []
  with open('/proc/meminfo', 'r') as proc_meminfo:
    for l in proc_meminfo.readlines():
      meminfo.append(l)

    for infos in [l.split() for l in meminfo]:
      if memory and infos[0] in ['MemTotal:']:
        ret[infos[0].split(":")[0]] = infos[1]
      if memory and infos[0] in ['MemAvailable:']:                                                                                                                                        
        ret['MemAvailable'] = infos[1]
      #On RHEL6 MemAvailable is not available and need to be computed (results do not match exactly)
      if memory and infos[0] in ['MemFree:','Buffers:', 'Cached:']:
        ret['MemAvailableComputed'] = str(int(ret.get('MemAvailableComputed', 0)) + int(infos[1]))
      if infos[0] in ['HugePages_Total:','HugePages_Free:', 'Hugepagesize:']:
        ret[infos[0].split(":")[0]] = infos[1]
      if swap and infos[0] in ['SwapTotal:','SwapFree:']:
        ret[infos[0].split(":")[0]] = infos[1]

  if not ret.get('MemAvailable'):
    ret['MemAvailable'] = ret['MemAvailableComputed']

  ret["processes"] = get_top_most_mem_procs(max_number_processes)
  return ret

def get_top_most_mem_procs(max_number):
  # Exeute  ps -hax -k -rss -o "comm rss pid args" to get sorted processes list 
  cmd=["ps", "-hax",  "-k" "-rss", "-o", "comm:15 rss pid args"]
  ps_cmd = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  output, error = ps_cmd.communicate()


  # Python3 reads the output as byte and needs decoding
  try:
    output = output.decode()
  except (UnicodeDecodeError, AttributeError):
    pass

  processes = []

  for ps_line in  output.splitlines()[:max_number]:
    # Split the lines and assign to variables (comm has a limit set to 16 chars - 1 for c string ending)
    splitted_line_without_comm  =  re.split("\s+", ps_line[16:], 2)
    splitted_line_without_comm.insert(0,ps_line[0:15])
    (name, rss, pid, args) = splitted_line_without_comm
    processes.append({"name": name, "pid": pid, "rss": rss, "cmdline": args})

  return processes

def main():

  args = dict(memory=dict(type='bool', default=True),
              swap=dict(type='bool', default=True),
              max_number_processes=dict(type='int', default=10)
              )

  module = AnsibleModule(
    argument_spec = args,
    supports_check_mode = True
  )

  memory = module.params['memory']
  swap = module.params['swap']
  max_number_processes = module.params['max_number_processes']
 
  try:
    result = dict(meminfo = get_memory_info(memory, swap, max_number_processes))
  except Exception as ex:
    module.fail_json(msg=ex)
  
  module.exit_json(**result)

if __name__ == '__main__':
  main()

