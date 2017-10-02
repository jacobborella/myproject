#!/usr/bin/python

from ansible.module_utils.basic import *
from subprocess import call, Popen

def main():
    fields = {
        "name": {"required": True, "type": "str"},
        "namespace": {"required": True, "type": "str"},
        "resource": {"required": True, "type": "str" },
        "vol-name": {"required": True, "type": "str"},
        "mount-path": {"required": True, "type": "str"},
        "type": {
            "default": "secret",
            "choices": ['secret'],
            "type": 'str'
        },
        "secret-name": {"required": False, "type": str},
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
    proc = Popen(['oc', 'volume', module.params['resource'] + '/' + module.params['name'], '-n', module.params['namespace'], '--name=' + module.params['vol-name']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = proc.communicate()
    vol_exists = proc.returncode == 0
    response['exists'] = vol_exists

    if 'present' == module.params['state']:
      if vol_exists:
        print 'todo'
      else:
        proc = Popen(['oc', 'volume', module.params['resource'] + '/' + module.params['name'], '--add', '-n', module.params['namespace'], '--name=' + module.params['vol-name'], '--type=' + module.params['type'], '--secret-name=' + module.params['secret-name'], '--mount-path=' + module.params['mount-path']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = proc.communicate()
        if proc.returncode == 0:
          changed = True
        else:
          response['err'] = stdout
    else:
      if vol_exists:
        proc = Popen(['oc', 'volume', module.params['resource'] + '/' + module.params['name'], '-n', module.params['namespace'], '--remove', '--name=' + module.params['vol-name']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = proc.communicate()
        changed = proc.returncode == 0



    module.exit_json(changed=changed, meta=response)


if __name__ == '__main__':  
    main()
