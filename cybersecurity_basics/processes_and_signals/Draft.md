Title: File is present
Label: Requirement
Eliminatory: true
Reason:
[files_exist] All files exist: 1-list_your_processes

Checker script:
files_exist(["1-list_your_processes"])
Title: First line contains #!/usr/bin/env bash
Label: Requirement
Eliminatory: true
Reason:
[file_contains_regex] Content of the file:
#!/usr/bin/env bash

Displays a list of currently running processes

ps auxH
[file_contains_regex] Pattern found: ^#!/usr/bin/env bash
Checker script:
file_contains_regex("1-list_your_processes", patterns=["^#!/usr/bin/env bash"])
Title: Second line contains a comment describing what your Bash script does
Label: Requirement
Eliminatory: true
Reason:
[exec_bash_compare] Command to run:
head -n 2 1-list_your_processes | tail -1 | head -c 1
su student_jail -c 'timeout 30 bash -c '"'"'head -n 2 1-list_your_processes | tail -1 | head -c 1'"'"''
[exec_bash_compare] Return code: 0
[exec_bash_compare] Student stdout:
#
[exec_bash_compare] Student stdout length: 1
[exec_bash_compare] Student stderr:
[exec_bash_compare] Student stderr length: 0
[exec_bash_compare] Desired stdout:
#
[exec_bash_compare] Desired stdout length: 1

Checker script:
exec_bash_compare("head -n 2 1-list_your_processes | tail -1 | head -c 1", "#")
Title: Your Bash script successfully passes `shellcheck`
Label: Requirement
Reason:
[shellcheck] Command to run:
shellcheck 1-list_your_processes
su student_jail -c 'timeout 30 bash -c '"'"'shellcheck 1-list_your_processes'"'"''
[shellcheck] Return code: 0
[shellcheck] Student stdout:
[shellcheck] Student stdout length: 0
[shellcheck] Student stderr:
[shellcheck] Student stderr length: 0

Checker script:
shellcheck(["1-list_your_processes"])
Title: Your Bash script return running processes according to requirements
Label: Requirement
Reason:
[exec_bash] Command to run:
./1-list_your_processes | awk '''{print $1, $9, $11, $12}''' | head -n 2
su student_jail -c 'timeout 30 bash -c '"'"'./1-list_your_processes | awk '"'"'"'"'"'"'"'"''"'"'"'"'"'"'"'"''"'"'"'"'"'"'"'"'{print $1, $9, $11, $12}'"'"'"'"'"'"'"'"''"'"'"'"'"'"'"'"''"'"'"'"'"'"'"'"' | head -n 2'"'"''
[exec_bash] Return code: 0
[exec_bash] Student stdout:
USER START COMMAND 
root 12:14 /bin/bash /checker/correction/main.sh
[exec_bash] Student stdout length: 69
[exec_bash] Student stderr:
[exec_bash] Student stderr length: 0
[exec_bash] Command to run:
ps auxf | awk '''{print $1, $9, $11, $12}''' | head -n 2
su student_jail -c 'timeout 30 bash -c '"'"'ps auxf | awk '"'"'"'"'"'"'"'"''"'"'"'"'"'"'"'"''"'"'"'"'"'"'"'"'{print $1, $9, $11, $12}'"'"'"'"'"'"'"'"''"'"'"'"'"'"'"'"''"'"'"'"'"'"'"'"' | head -n 2'"'"''
[exec_bash] Return code: 0
[exec_bash] Student stdout:
USER START COMMAND 
root 12:14 /bin/bash /checker/correction/main.sh
[exec_bash] Student stdout length: 69
[exec_bash] Student stderr:
[exec_bash] Student stderr length: 0

Checker script:
(exec_bash("./1-list_your_processes | awk '\''{print $1, $9, $11, $12}'\'' | head -n 2") == exec_bash("ps auxf | awk '\''{print $1, $9, $11, $12}'\'' | head -n 2"))