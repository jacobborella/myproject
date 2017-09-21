#!/usr/bin/python

from ansible.module_utils.basic import *
from subprocess import call, Popen

def main():
    fields = {
        "filename": {"required": True, "type": "str"},
        "namespace": {"required": True, "type": "str"},
        "state": {
            "default": "present", 
            "choices": ['present', 'absent'],  
            "type": 'str' 
        },
    }

    module = AnsibleModule(argument_spec=fields)
    response = {}
    changed = False

    #investigate whether the template already exists
    proc = Popen(['oc', 'get', '-f', module.params['filename'], '-n', module.params['namespace']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = proc.communicate()
    exists = proc.returncode == 0

    #investigate whether the template has changed since last time if it exists
    #calc md5 for new file https://gist.github.com/aseigneurin/4902819f17218340d11f
    #label template with md5
    #compare md5 by getting label - compare to new file
    #light version is using md5 for tmp file if file doesn't exists file have changed (not as secure obviously)
    template_changed = True

    #if not and template must be there, create the template
    if not exists and 'present' == module.params['state']: 
      proc = Popen(['oc', 'create', '-f', module.params['filename'], '-n', module.params['namespace']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      stdout, stderr = proc.communicate()
      if proc.returncode == 0:
        changed = True
      else:
        module.fail_json(msg=stdout)
        
    if exists and template_changed:
      proc = Popen(['oc', 'replace', '-f', module.params['filename'], '-n', module.params['namespace']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      stdout, stderr = proc.communicate()
      changed = True

    if 'absent' == module.params['state']:
      proc = Popen(['oc', 'delete', '-f', module.params['filename'], '-n', module.params['namespace']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      stdout, stderr = proc.communicate()
      changed = True
       

    module.exit_json(changed=changed, meta=response)


if __name__ == '__main__':  
    main()
