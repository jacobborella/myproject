#!/usr/bin/python

from ansible.module_utils.basic import *
from subprocess import call, Popen

def main():
    fields = {
        "name": {"required": True, "type": "str"},
        "namespace": {"required": True, "type": "str"},
        "resource": {"required": True, "type": "str" },
        "key": {"required": True, "type": str},
        "value": {"required": False, "type": "str"},
        "state": {
            "default": "present", 
            "choices": ['present', 'absent'],  
            "type": 'str' 
        },
    }

    module = AnsibleModule(argument_spec=fields)
    response = {}
    changed = False

    #decide whether env variable exists
    proc = Popen(['oc', 'env', module.params['resource'] + '/' + module.params['name'], '-n', module.params['namespace'], '--list'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = proc.communicate()
    keyIdx = stdout.find(module.params['key'])
    valIdx = stdout.find('=', keyIdx) + 1
    currentValue = stdout[valIdx:stdout.find('\n', keyIdx)] 
    print currentValue
    env_exists = proc.returncode == 0 and len(stdout) > 0 and keyIdx > 0
    response['exists'] = env_exists

    if 'present' == module.params['state']:
      #env variable must be there
      if currentValue != str(module.params['value']):
        #variable has changed since last time update it
        proc = Popen(['oc', 'env', module.params['resource'] + '/' + module.params['name'], '-n', module.params['namespace'], str(module.params['key']) + '=' + str(module.params['value'])], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = proc.communicate()
        changed = True
    else:
      if env_exists:
        #variable is there, but marked absent -> delete it
        changed = True
        proc = Popen(['oc', 'env', module.params['resource'] + '/' + module.params['name'], '-n', module.params['namespace'], str(module.params['key']) + '-'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = proc.communicate()




    module.exit_json(changed=changed, meta=response)


if __name__ == '__main__':  
    main()
