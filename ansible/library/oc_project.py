#!/usr/bin/python

from ansible.module_utils.basic import *
from subprocess import call, Popen

def main():
    fields = {
        "name": {"required": True, "type": "str" },
        "displayName": {"required": False, "type": "str"},
        "description": {"required": False, "type": "str"},
        "state": {
            "default": "present", 
            "choices": ['present', 'absent'],  
            "type": 'str' 
        },
    }

    module = AnsibleModule(argument_spec=fields)
    response = {}

    #decide whether project exists
    #use oc get project ansibletestproject -o yaml instead and decide if there are changes as well
    proc = Popen(['oc', 'project', module.params['name']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    proc.communicate()
    project_exists = proc.returncode

    changed = False


    if 'present' == module.params['state'] and project_exists > 0:
      #project doesn't exist, create it
      proc = Popen(['oc', 'new-project', module.params['name']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
      stdout, stderr = proc.communicate()
      if proc.returncode == 0:
        changed = True
      else:
        module.fail_json(msg=stdout)
    if 'absent' == module.params['state'] and project_exists == 0:
      #project exists, delete it
      proc = Popen(['oc', 'delete', 'project', module.params['name']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      stdout, stderr = proc.communicate()
      if proc.returncode == 0:
        changed = True
      else:
        module.fail_json(msg=stdout)






    module.exit_json(changed=changed, meta=response)


if __name__ == '__main__':  
    main()
