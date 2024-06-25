#!/usr/bin/python

import os 
from ansible.module_utils.basic import AnsibleModule


def get_fileinfo(filepath):
  isfile = os.path.isfile(filepath)
  if isfile:
    statinfo = os.stat(filepath)
    return {
      "status" : 0,
      "st_mtime": statinfo.st_mtime,
      "st_size": statinfo.st_size
    }
  else:
    return {
      "status" : 1
    }   

def main():
  module_args= dict(
  filepath = dict(type='str', required=True)
)

  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True
  )

  filepath = module.params['filepath']
  fileinfo = get_fileinfo(filepath)
  
  try:
    result = dict(fileinfo=fileinfo)
  except Exception as ex:
    module.fail_json(msg=str(ex))

  module.exit_json(**result)

if __name__ == '__main__':
  main()

