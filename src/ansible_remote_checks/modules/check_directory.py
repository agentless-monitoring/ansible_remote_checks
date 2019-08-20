#!/usr/bin/python2

import os 
import re
from ansible.module_utils.basic import AnsibleModule

def get_directory_info(path, recursive=False, file_regex='.*'):

  result = []

  for root, d_names, f_names in os.walk(path):
    if not recursive:
      for file_name in f_names:
        if re.match(file_regex, file_name):
          statinfo = os.stat(os.path.join(path, file_name))
          result.append({"name": file_name,  "st_mtime": statinfo.st_mtime,"st_size": statinfo.st_size})
      break
      
    else:
      if (len(f_names) == 0):
        continue
      for file_name in f_names:
         name = os.path.relpath(root + "/" + file_name, path)
         if re.match(file_regex, name):
           statinfo = os.stat(os.path.join(path, name))
           result.append({"name": name,  "st_mtime": statinfo.st_mtime,"st_size": statinfo.st_size})

  return result

def main():
  module_args= dict(
  path = dict(type='str', required=True),
  regex = dict(type='str'),
  recursive = dict(type='bool')
)

  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True
  )

  path = module.params['path']
  file_regex = module.params['regex']
  recursive = module.params['recursive']

  fileinfo = get_directory_info(path, recursive, file_regex)
  
  try:
    result = dict(fileinfo=fileinfo)
  except Exception as ex:
    module.fail_json(msg=str(ex))

  module.exit_json(**result)

if __name__ == '__main__':
  main()

