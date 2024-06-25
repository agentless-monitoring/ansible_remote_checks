#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

import os
from datetime import datetime

def count_files(path, min_age):
  current_time = datetime.now()
  count = 0
  for f in os.listdir(path):
    fullpath = os.path.join(path, f)
    if os.path.isfile(fullpath) is False:
        continue
    stats = os.stat(fullpath)
    mtime=datetime.fromtimestamp(stats.st_mtime)
    lastchanged_minutes=int((current_time-mtime).total_seconds()/60)
    if (lastchanged_minutes >= min_age):
      count = count + 1

  return {"file_count": count}


def main():
  module_args= dict(
    path = dict(type='str', required=True),
    min_age = dict(type='int', default=0)
  )

  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True
  )

  path = module.params['path']
  min_age = module.params['min_age']
  try:
    result = count_files(path, min_age)
  except Exception as ex:
    module.fail_json(msg=str(ex))

  module.exit_json(**result)

if __name__ == "__main__":
  main()
