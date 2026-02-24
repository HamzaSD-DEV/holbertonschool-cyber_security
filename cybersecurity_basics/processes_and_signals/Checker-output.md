Title: File is present
Label: Requirement
Eliminatory: true
Reason:
[files_exist] All files exist: 0-what-is-my-pid

Checker script:
files_exist(["0-what-is-my-pid"])
Title: README.md exists and is not empty
Label: Requirement
Eliminatory: true
Reason:
[files_exist] All files exist: README.md
[files_empty] File not empty: README.md
[files_exist] All files exist: README.md
[files_empty] File not empty: README.md

Checker script:
((files_exist(["README.md"]) and (not files_empty(["README.md"]))) and (files_exist(["README.md"]) and (not files_empty(["README.md"]))))
Title: First line contains #!/usr/bin/env bash
Label: Requirement
Eliminatory: true
Reason:
[file_contains_regex] Content of the file:
#!/usr/bin/env bash

Displays the current process ID (PID)

echo $$
[file_contains_regex] Pattern found: ^#!/usr/bin/env bash
Checker script:
file_contains_regex("0-what-is-my-pid", patterns=["^#!/usr/bin/env bash"])
Title: Second line contains a comment describing what your Bash script does
Label: Requirement
Eliminatory: true
Reason:
[exec_bash_compare] Command to run:
head -n 2 0-what-is-my-pid | tail -1 | head -c 1
su student_jail -c 'timeout 30 bash -c '"'"'head -n 2 0-what-is-my-pid | tail -1 | head -c 1'"'"''
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
exec_bash_compare("head -n 2 0-what-is-my-pid | tail -1 | head -c 1", "#")
Title: Your Bash script successfully passes `shellcheck`
Label: Requirement
Reason:
[shellcheck] Command to run:
shellcheck 0-what-is-my-pid
su student_jail -c 'timeout 30 bash -c '"'"'shellcheck 0-what-is-my-pid'"'"''
[shellcheck] Return code: 0
[shellcheck] Student stdout:
[shellcheck] Student stdout length: 0
[shellcheck] Student stderr:
[shellcheck] Student stderr length: 0

Checker script:
shellcheck(["0-what-is-my-pid"])
Title: Your Bash script returns its PID
Label: Code
Reason:
[exec_bash_compare] Command to run:
head -n 2 0-what-is-my-pid | tail -1 | head -c 1
su student_jail -c 'timeout 30 bash -c '"'"'head -n 2 0-what-is-my-pid | tail -1 | head -c 1'"'"''
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
exec_bash_compare("head -n 2 0-what-is-my-pid | tail -1 | head -c 1", "#")
