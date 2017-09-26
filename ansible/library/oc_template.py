#!/usr/bin/python

from ansible.module_utils.basic import *
from subprocess import call, Popen
import yaml

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

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

    #if not and template must be there, create the template
    if 'present' == module.params['state']:
      #extract new template version
      newTemplateVersion = md5(module.params['filename'])
      if exists:
        #investigate whether the template has changed since last time if it exists
        proc = Popen(['oc', 'get', '-f', module.params['filename'], '-o', 'yaml', '-n', module.params['namespace']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = proc.communicate()
        if proc.returncode == 0:
          #extract version of currently used template
          templateDoc = yaml.load(stdout)
          oldTemplateVersion = templateDoc['metadata']['labels']['template-version']
          response['old-template-version'] = oldTemplateVersion
        else:
          module.fail_json(msg=stdout)
        
        if oldTemplateVersion != newTemplateVersion:
          proc = Popen(['oc', 'apply', '-f', module.params['filename'], '-n', module.params['namespace']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
          stdout, stderr = proc.communicate()
          proc = Popen(['oc', 'label', '-f', module.params['filename'], '-n', module.params['namespace'], 'template-version=' + str(newTemplateVersion)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
          stdout, stderr = proc.communicate()
          changed = True
      else: 
        proc = Popen(['oc', 'create', '-f', module.params['filename'], '-n', module.params['namespace']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = proc.communicate()
        proc = Popen(['oc', 'label', '-f', module.params['filename'], '-n', module.params['namespace'], 'template-version=' + str(newTemplateVersion)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = proc.communicate()
        if proc.returncode == 0:
          changed = True
        else:
          module.fail_json(msg=stdout)

    if 'absent' == module.params['state'] and exists:
      proc = Popen(['oc', 'delete', '-f', module.params['filename'], '-n', module.params['namespace']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      stdout, stderr = proc.communicate()
      changed = True

      

    module.exit_json(changed=changed, meta=response)


if __name__ == '__main__':  
    main()
