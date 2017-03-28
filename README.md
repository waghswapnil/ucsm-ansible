```
➔ ansible-playbook -i inventory site.yml

PLAY [ucs] *********************************************************************

TASK [common : check if ucsmsdk is installed] **********************************
ok: [localhost]

TASK [common : install ucsmsdk] ************************************************
skipping: [localhost]

TASK [common : check if ucsm_apis is installed] ********************************
ok: [localhost]

TASK [common : clone ucsm_apis] ************************************************
skipping: [localhost]

TASK [common : install ucsm_apis] **********************************************
skipping: [localhost]

TASK [power : power on server] *************************************************
changed: [localhost]

PLAY RECAP *********************************************************************
localhost                    : ok=3    changed=1    unreachable=0    failed=0

```
