#!/usr/bin/python

from ansible.module_utils.basic import *
from subprocess import call, Popen

def main():
    fields = {
        "name": {"required": True, "type": "str"},
        "namespace": {"required": True, "type": "str"},
        "git-repo": {"required": False, "type": "str" },
        "template": {"required": False, "type": str},
        "template-parameters": {"required": False, "type": "str"},
        "state": {
            "default": "present", 
            "choices": ['present', 'absent'],  
            "type": 'str' 
        },
    }

    module = AnsibleModule(argument_spec=fields)
    response = {}

    #decide whether app exists
    proc = Popen(['oc', 'get', 'svc', '--selector=app=' + module.params['name'], '-n', module.params['namespace']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = proc.communicate()
    app_exists = proc.returncode == 0 and len(stdout) > 0 and not stdout.startswith('No resources found.')

    changed = False

    if 'present' == module.params['state'] and not app_exists:
      #app doesn't exist, create it
      proc_values = ['oc', 'new-app']
      if module.params['template'] is None:
        proc_values.append(module.params['git-repo'])
      else:
        proc_values.append(module.params['template'])

      if not(module.params['template-parameters'] is None):
        templateParameters = module.params['template-parameters'].split(',')
        for templateParameter in templateParameters:
          proc_values.append('-p')
          proc_values.append(templateParameter)


      proc_values.extend(['-l', 'app=' + module.params['name'] ,'--name', module.params['name'], '-n', module.params['namespace']])
      proc = Popen(proc_values, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
      stdout, stderr = proc.communicate()
      if proc.returncode == 0:
        changed = True
      else:
        module.fail_json(msg=stdout)
    if 'absent' == module.params['state'] and app_exists:
      # app exists, delete it
      proc = Popen(['oc', 'delete', 'all', '--selector=app=' + module.params['name'], '-n', module.params['namespace']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      stdout, stderr = proc.communicate()
      if proc.returncode == 0:
        changed = True
      else:
        module.fail_json(msg=stdout)






    module.exit_json(changed=changed, meta=response)


if __name__ == '__main__':  
    main()
