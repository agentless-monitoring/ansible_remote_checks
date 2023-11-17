#!/usr/bin/python

import os
import subprocess
import re
from ansible.module_utils.basic import AnsibleModule

def get_sg_info():
  
  cmd = "cmviewcl -f line"
  process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  returncode = process.returncode

   # Python3 reads the output as byte and needs decoding
  try:
    output = output.decode()
  except (UnicodeDecodeError, AttributeError):
    pass

  result = {}
  result['output'] = {}
  result['output']['packages'] = {}
  result['output']['cluster'] = {}
  result['output']['nodes'] = {} 
  regex_package_node = r'package:(.*)[|]node:(.*)[|](.*)=(.*)'
  regex_package = r'package:(.*)[|](.*)=(.*)'
  regex_node = r'node:(.*)[|](.*)=(.*)' 
  regex_cluster = r'(.*)=(.*)'

  
  lines = output.splitlines()
  for line in lines:
    search = re.search(regex_package_node, line)
    if search:
      group = search.groups()
      if not result['output']['packages'][group[0]].get(group[1]):                                                                                                                        
        result['output']['packages'][group[0]][group[1]]={} 
    
      result['output']['packages'][group[0]][group[1]][group[2]]=group[3]

    elif re.search(regex_package, line):
      group = re.search(regex_package, line).groups()
      if not result['output']['packages'].get(group[0]):                                                                                                                                
        result['output']['packages'][group[0]]={}
     
      result['output']['packages'][group[0]][group[1]]=group[2]
   
    elif re.search(regex_node, line):                                                                                                                                                  
      group = re.search(regex_node, line).groups() 

      if not result['output']['nodes'].get(group[0]):                                                                                                                      
        result['output']['nodes'][group[0]]={}
                                                                                                                                      
      result['output']['nodes'][group[0]][group[1]]=group[2]         

    elif re.search(regex_cluster, line):
      group = re.search(regex_cluster, line).groups()                                                                                                                                     
      result['output']['cluster'][group[0]]=group[1]        
  
  return result

def main():

  module = AnsibleModule(
    argument_spec = dict(),
    supports_check_mode = True
  )
 
  try: 
    result = dict(sg_info = get_sg_info())
  except Exception as ex:
    module.fail_json(msg=str(ex))
 
  module.exit_json(**result) 

if __name__ == '__main__':
  main()
