#!/usr/bin/python

import re
import os
from ansible.module_utils.basic import AnsibleModule

def get_fs_usage(filesystem):
  with open('/etc/mtab', 'r') as mtab:
    ret = {}
    seen = {}
    for mnt in [l.split() for l in  mtab.readlines()]:
      #  With bind mounts, prefer items nearer the root of the source
      if mnt[0] not in seen or len(mnt[1]) < len(seen[mnt[0]]):
        seen[mnt[0]] = mnt[1]

    for key,value in seen.items():
      stat = {}
      if (filesystem and re.match(r"%s" % filesystem, value)) or (not filesystem and (key.startswith('/dev/sd') or key.startswith('/dev/mapper') or key.startswith('/dev/md'))):
        try:
          stat = os.statvfs(value)
          total_byte = stat.f_blocks * stat.f_frsize
          free_byte = stat.f_bavail * stat.f_frsize
          used_percent = 0
         
          if stat.f_blocks > 0:
            used_percent = int(round((1 - float(stat.f_bavail) / float(stat.f_blocks)) * 100))            
         
          mount_flags = stat.f_flag
          ret[value] = {
            "total_byte": total_byte,
            "free_byte": free_byte,
            "used_percent": used_percent,
            "mount_flags" : mount_flags
            }
        except Exception as e:
          ret[value] = {
            "total_byte" : 0,
            "free_byte" : 0,
            "used_percent" : 0,
            "mount_flags" : 0,
            "skipped": str(e)
           }
        
  return ret

def main():

  args = dict(filesystem=dict(type='str'))

  module = AnsibleModule(
    argument_spec = args,
    supports_check_mode = True
  )

  filesystem = module.params['filesystem']

  try:
    result = dict(file_systems = get_fs_usage(filesystem))
  except Exception as ex:
    module.fail_json(msg=str(ex))  

  module.exit_json(**result)

if __name__ == '__main__':
  main()

