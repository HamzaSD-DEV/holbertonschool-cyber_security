
<!-- TOC ignore:true -->
# Checker v2 functions

This repository contains Checker v2 functions and Docker images for the
Checker v2.

<!-- TOC ignore:true -->
## Table of Contents

<!-- TOC -->

- [Usage](#usage)
    - [Output](#output)
- [Built-in operators](#built-in-operators)
- [Functions](#functions)
- [Docker images](#docker-images)
- [Checker v1 to Checker v2](#checker-v1-to-checker-v2)
    - [Translate single command](#translate-single-command)
    - [Translate commands from CSV](#translate-commands-from-csv)
    - [Function mapping](#function-mapping)

<!-- /TOC -->

# Usage

New checker commands are written in Python.

All built-in checker functions are inside `checker_functions` folder and can be
used inside checker commands without any setup needed. Below you can find the
[description and usage](#functions) of each function. You can also find the
[translation](#checker-v1-to-checker-v2) of the older checker functions to the
new ones below.

## Output

The full checker command will be evaluated to boolean to determine whether the
checker command passes or not. For example, if you want to use `files_exists`
(that returns `True` or `False`), your checker command will look like this:
```
files_exists(["file1", "file2"])
```

Note that if your top-level function returns a string or a number, the return
value will be evaluated with `bool()`. For example, if your function is:
```
file_content("file1")
```
It will pass the checker if the file content is not empty.

# Built-in operators

Various python operators can be used together with functions.

<!-- TOC ignore:true -->
## Not

```
not files_exist(["file1.txt])
```

<!-- TOC ignore:true -->
## And

```
files_exist(["file1.txt]) and files_empty(["file1.txt])
```

<!-- TOC ignore:true -->
## Or

```
files_exist(["file_or_folder"]) or folders_exist(["file_or_folder"])
```

<!-- TOC ignore:true -->
## Addition

```
5 + 2
```

<!-- TOC ignore:true -->
## Subtraction

```
5 - 2
```

<!-- TOC ignore:true -->
## Mutliplication

```
2 * 3
```

<!-- TOC ignore:true -->
## Mod

```
5 % 2
```

<!-- TOC ignore:true -->
## Equal

```
"hello" == "hello world"
```

<!-- TOC ignore:true -->
## Not equal

```
"hello" != "hello world"
```

<!-- TOC ignore:true -->
## Less

```
1 < 2
```

<!-- TOC ignore:true -->
## Less or equal

```
1 <= 2
```

<!-- TOC ignore:true -->
## Greater

```
1 > 2
```

<!-- TOC ignore:true -->
## Greater or equal

```
1 >= 2
```

# Functions

Paths from student repo should be relative to the `github_folder` provided
during checker request.

Paths for the checker correction files should be relative to the `corrections`
[folder](https://github.com/hs-hq/corrections_hbtn/tree/main/corrections).

---

<!-- TOC ignore:true -->
## lazy_int

> Tries to convert a string to an int, otherwise returns 0

*Parameters:*

* **string** (`str`): A string to convert to integer

*Returns:*

* (`int`) Integer parsed from the string, otherwise 0 

---

<!-- TOC ignore:true -->
## number_of_occurrences

> Returns number of occurrences of a pattern in a given file.

*Parameters:*

* **path** (`str`): File path relative to the student github folder
* **pattern** (`str`): Pattern to be searched for
* **case_sensitive** (`bool = True`): Whether perform a case-sensitive search

*Returns:*

* (`int`) Number of occurrences of a pattern in a given file as a number. 

---

<!-- TOC ignore:true -->
## folders_exist

> Checks if all folders exist.

*Parameters:*

* **paths** (`list[str]`): List of folder paths relative to the student github folder

*Returns:*

* (`bool`) True if all folders exist, otherwise False 

---

<!-- TOC ignore:true -->
## files_exist

> Checks if all files exist.

*Parameters:*

* **paths** (`list[str]`): List of file paths relative to the student github folder

*Returns:*

* (`bool`) True if all files exist, otherwise False 

---

<!-- TOC ignore:true -->
## files_empty

> Checks if all files are empty.

*Parameters:*

* **paths** (`list[str]`): List of file paths relative to the student github folder

*Returns:*

* (`bool`) True if all files are empty, otherwise False 

---

<!-- TOC ignore:true -->
## copy_files

> Copies files or folders from checker correction folder to the student github folder.

*Parameters:*

* **paths** (`list[str]`): List of file or folder paths relative to the checker correction folder or absolute paths in the checker docker image

*Returns:*

* (`bool`) True if all files were copied successfully, otherwise False 

---

<!-- TOC ignore:true -->
## copy_and_replace_file

> Copies student file and replaces substring.

*Parameters:*

* **path** (`str`): File path relative to the student github folder
* **search_string** (`str`): Substring to search for
* **replace_string** (`str`): String to replace
* **output_path** (`str`): File path relative to the student github folder

*Returns:*

* (`bool`) True if file was copied successfully, otherwise False 

---

<!-- TOC ignore:true -->
## number_of_lines

> Returns number of lines in the file.

*Parameters:*

* **path** (`str`): File path relative to the student github folder

*Returns:*

* (`int`) Number of lines in the file. If the file is not found, returns 0. 

---

<!-- TOC ignore:true -->
## valid_number_of_lines

> Checks if the file contains the expected number of lines.

*Parameters:*

* **path** (`str`): File path relative to the student github folder
* **number_of_lines** (`int`): Expected number of lines

*Returns:*

* (`bool`) True if the file contains an expected number of lines, otherwise False. If the file is not found, returns False. 

---

<!-- TOC ignore:true -->
## compare_preload

> Runs the command with the preloaded library and compares stdout and stderr.

*Parameters:*

* **library_path** (`str`): Library path relative to the checker corrections folder
* **command** (`str`): Bash command to be executed
* **desired_output_path** (`str`): Path in the checker corrections folder of the desired stdout
* **desired_error_path** (`Optional[str] = None`): Path in the checker corrections folder of the desired stderr
* **with_root** (`bool = True`): Whether to execute the command with root user
* **timeout** (`int = 30`): Deadline of the command in seconds

*Returns:*

* (`bool`) True if the stdout and stderr of the command are as desired, otherwise False 

---

<!-- TOC ignore:true -->
## compare

> Runs the command and compares stdout and stderr.

*Parameters:*

* **command** (`str`): Bash command to be executed
* **desired_output_path** (`str`): Path in the checker corrections folder of the desired stdout
* **desired_error_path** (`Optional[str] = None`): Path in the checker corrections folder of the desired stderr
* **with_root** (`bool = True`): Whether to execute the command with root user
* **timeout** (`int = 30`): Deadline of the command in seconds

*Returns:*

* (`bool`) True if the stdout and stderr of the command are as desired, otherwise False 

---

<!-- TOC ignore:true -->
## malloc

> Checks if the command has segmentation fault with fake malloc library.

*Parameters:*

* **command** (`str`): Binary path relative to the student github folder
* **library_path** (`str`): Fake malloc library path
* **timeout** (`int = 30`): Deadline of the command in seconds

*Returns:*

* (`bool`) True if the command does not throw segmentation fault, otherwise False 

---

<!-- TOC ignore:true -->
## make

> Executes make command.

*Parameters:*

* **rule** (`str = "all"`): Make rule to build
* **makefile_path** (`str = "Makefile"`): Path of the Makefile relative to the student github folder
* **options** (`str = ""`): Options to pass to the make command
* **timeout** (`int = 30`): Deadline for the make command in seconds

*Returns:*

* (`bool`) True if the make command executes successfully, otherwise False 

---

<!-- TOC ignore:true -->
## preprocessed_does_not_contain

> Checks if the preprocessed c file does not contain any specified patterns.

*Parameters:*

* **path** (`str`): Path to the preprocessed c file relative to the student github folder
* **patterns** (`list[str]`): List of regex patterns to check

*Returns:*

* (`bool`) True if none of the patterns are present in the preprocessed c file, otherwise False 

---

<!-- TOC ignore:true -->
## contains

> Checks if a string contains all specified substrings.

*Parameters:*

* **content** (`str`): String to check
* **patterns** (`list[str]`): List of substrings to check

*Returns:*

* (`bool`) True all substrings are present in the string, otherwise False 

---

<!-- TOC ignore:true -->
## file_contains

> Checks if a file contains all specified substrings.

*Parameters:*

* **path** (`str`): File path relative to the student github folder
* **patterns** (`list[str]`): List of substrings to check
* **ignore_docstrings** (`bool = False`): Whether to ignore content within python docstrings.

*Returns:*

* (`bool`) True all substrings are present in the file, otherwise False 

---

<!-- TOC ignore:true -->
## file_contains_regex

> Checks if a file contains all specified patterns.

*Parameters:*

* **path** (`str`): File path relative to the student github folder
* **patterns** (`list[str]`): List of regex patterns to check
* **case_sensitive** (`bool = True`): Whether to use case-sensitive regex matching
* **multiline** (`bool = False`): Whether to allow regex to match dot across multiple lines
* **ignore_docstrings** (`bool = False`): Whether to ignore content within python docstrings.

*Returns:*

* (`bool`) True all patterns are present in the file, otherwise False 

---

<!-- TOC ignore:true -->
## file_does_not_contain

> Checks if a file does not contain all specified substrings.

*Parameters:*

* **path** (`str`): File path relative to the student github folder
* **patterns** (`list[str]`): List of substrings to check

*Returns:*

* (`bool`) True all substrings are not present in the file, otherwise False 

---

<!-- TOC ignore:true -->
## file_content

> Returns the content of the file.

*Parameters:*

* **path** (`str`): File path relative to the student github folder

*Returns:*

* (`str`) Content of the file. 

---

<!-- TOC ignore:true -->
## exec_bash

> Executes bash command and returns stdout.

*Parameters:*

* **command** (`str`): Bash command to be executed
* **with_root** (`bool = True`): Whether to execute the command with root user
* **timeout** (`int = 30`): Deadline of the command in seconds

*Returns:*

* (`str`) Output of the command 

---

<!-- TOC ignore:true -->
## exec_bash_ignore_errors

> Executes bash command and always returns True.

*Parameters:*

* **command** (`str`): Bash command to be executed
* **with_root** (`bool = True`): Whether to execute the command with root user
* **timeout** (`int = 30`): Deadline of the command in seconds

*Returns:*

* (`bool`) True 

---

<!-- TOC ignore:true -->
## exec_bash_success

> Executes bash command and checks if it executed successfully.

*Parameters:*

* **command** (`str`): Bash command to be executed
* **with_root** (`bool = True`): Whether to execute the command with root user
* **timeout** (`int = 30`): Deadline of the command in seconds

*Returns:*

* (`bool`) True if the command executes successfully, otherwise False 

---

<!-- TOC ignore:true -->
## exec_bash_compare

> Executes bash command and returns stdout.

*Parameters:*

* **command** (`str`): Bash command to be executed
* **desired_output** (`str`): Expected output of the bash command
* **with_root** (`bool = True`): Whether to execute the command with root user
* **timeout** (`int = 30`): Deadline of the command in seconds

*Returns:*

* (`bool`) True if the output is as desired, otherwise False 

---

<!-- TOC ignore:true -->
## exec_bash_contains

> Executes bash command and checks if stdout contains all specified substrings.

*Parameters:*

* **command** (`str`): Bash command to be executed
* **patterns** (`list[str]`): List of substrings to check
* **with_root** (`bool = True`): Whether to execute the command with root user
* **timeout** (`int = 30`): Deadline of the command in seconds

*Returns:*

* (`bool`) True if all substrings are present in the stdout, otherwise False 

---

<!-- TOC ignore:true -->
## container_valid

> Checks if the student container can be connected to.

*Returns:*

* (`bool`) True if can connect to the student container, otherwise False 

---

<!-- TOC ignore:true -->
## container_exec_bash

> Executes bash command inside the student container and returns stdout.

*Parameters:*

* **command** (`str`): Bash command to be executed
* **timeout** (`int = 30`): Deadline for the bash command in seconds (note that it's a timeout for a single bash command, the full execution of the function can be longer due to retries)
* **retries** (`int = 5`): Number of retries if encounters ssh connection errors or timeout
* **sleep_between_retries** (`int = 5`): Number of seconds to wait before retrying

*Returns:*

* (`str`) Output of the command 

---

<!-- TOC ignore:true -->
## container_exec_bash_success

> Checks that the bash command run inside the student container is successful.

*Parameters:*

* **command** (`str`): Bash command to be executed
* **timeout** (`int = 30`): Deadline for the bash command in seconds (note that it's a timeout for a single bash command, the full execution of the function can be longer due to retries)
* **retries** (`int = 5`): Number of retries if encounters ssh connection errors or timeout
* **sleep_between_retries** (`int = 5`): Number of seconds to wait before retrying

*Returns:*

* (`bool`) True if the bash command succeeded, otherwise False 

---

<!-- TOC ignore:true -->
## container_exec_bash_compare

> Checks that the bash command run inside the student container has desired output.

*Parameters:*

* **command** (`str`): Bash command to be executed
* **desired_output** (`str`): Expected output of the bash command
* **timeout** (`int = 30`): Deadline for the bash command in seconds (note that it's a timeout for a single bash command, the full execution of the function can be longer due to retries)
* **retries** (`int = 5`): Number of retries if encounters ssh connection errors or timeout
* **sleep_between_retries** (`int = 5`): Number of seconds to wait before retrying

*Returns:*

* (`bool`) True if the output matches the desired output, otherwise False 

---

<!-- TOC ignore:true -->
## container_exec_bash_contains

> Executes bash command inside the student container and checks if stdout contains all specified substrings.

*Parameters:*

* **command** (`str`): Bash command to be executed
* **patterns** (`list[str]`): List of substrings to check
* **timeout** (`int = 30`): Deadline for the bash command in seconds (note that it's a timeout for a single bash command, the full execution of the function can be longer due to retries)
* **retries** (`int = 5`): Number of retries if encounters ssh connection errors or timeout
* **sleep_between_retries** (`int = 5`): Number of seconds to wait before retrying

*Returns:*

* (`bool`) True if all substrings are present in the stdout, otherwise False 

---

<!-- TOC ignore:true -->
## sass_compile

> Compiles Sass files and checks if compilation succeeded.

*Parameters:*

* **paths** (`list[str]`): Path to files relative to the student github folder or to the checker corrections folder
* **output_name** (`str`): Name of the output file
* **options** (`Optional[str] = None`): Options to pass to sass command
* **timeout** (`int = 30`): Deadline of the command in seconds

*Returns:*

* (`bool`) True if compilation succeeded, otherwise False 

---

<!-- TOC ignore:true -->
## gcc

> Executes gcc command and checks that it executed successfully.

*Parameters:*

* **paths** (`list[str]`): Path to files relative to the student github folder or to the checker corrections folder
* **output_name** (`str = "a.out"`): Name of the output file
* **options** (`str = "-Wall -Werror -Wextra -pedantic"`): Options to pass to gcc command
* **skip_warning** (`bool = False`): Whether to skip warnings
* **timeout** (`int = 30`): Deadline of the command in seconds

*Returns:*

* (`bool`) True if the command was executed successfully, otherwise False 

---

<!-- TOC ignore:true -->
## valgrind_leak

> Checks if there are any valgrind leaks in the command.

*Parameters:*

* **command** (`str`): Command to execute and check for leaks
* **timeout** (`int = 10`): Deadline of the command in seconds

*Returns:*

* (`bool`) True if there are any leaks, otherwise False 

---

<!-- TOC ignore:true -->
## valgrind_error

> Checks if there are any valgrind errors in the command.

*Parameters:*

* **command** (`str`): Command to execute and check for valgrind errors
* **timeout** (`int = 10`): Deadline of the command in seconds

*Returns:*

* (`bool`) True if there are any valgrind errors, otherwise False 

---

<!-- TOC ignore:true -->
## valgrind_allocations

> Returns number of bytes allocated in the command.

*Parameters:*

* **command** (`str`): Command to execute and check for leaks
* **timeout** (`int = 10`): Deadline of the command in seconds

*Returns:*

* (`int`) Number of bytes allocated 

---

<!-- TOC ignore:true -->
## ltrace_allowed

> Checks if binary contains only allowed functions.

*Parameters:*

* **command** (`str`): Command to execute
* **allowed_functions** (`list[str]`): List of allowed functions
* **timeout** (`int = 10`): Deadline of the command in seconds

*Returns:*

* (`bool`) True if binary contains only allowed functions, otherwise False 

---

<!-- TOC ignore:true -->
## ltrace_not_allowed

> Checks if binary doesn not contain not allowed functions.

*Parameters:*

* **command** (`str`): Command to execute
* **not_allowed_functions** (`list[str]`): List of not allowed functions
* **timeout** (`int = 10`): Deadline of the command in seconds

*Returns:*

* (`bool`) True if binary does not contain not allowed functions, otherwise False 

---

<!-- TOC ignore:true -->
## ltrace_count

> Checks number of calls of the specified function.

*Parameters:*

* **command** (`str`): Command to execute
* **function** (`str`): Function to trace
* **timeout** (`int = 10`): Deadline of the command in seconds

*Returns:*

* (`int`) Number of calls to the specified function 

---

<!-- TOC ignore:true -->
## semistandard

> Checks if javascript files are following Semi-Standard style.

*Parameters:*

* **paths** (`list[str]`): List of file paths relative to the student github folder
* **options** (`Optional[list[str]] = None`): Options to pass to the semistandard command

*Returns:*

* (`bool`) True if all files follow semi-standrad style, otherwise False 

---

<!-- TOC ignore:true -->
## node_lint

> Verifies that files are following node lint format.

*Parameters:*

* **paths** (`list[str]`): Paths to files to be checked

*Returns:*

* (`bool`) True if all files follow node lint format, otherwise False 

---

<!-- TOC ignore:true -->
## py_unittests

> Checks if all unit tests pass.

*Parameters:*

* **path** (`str`): Path to the test file or directory with tests relative to the student github folder
* **options** (`str = ""`): Bash variables to declare before running the tests

*Returns:*

* (`bool`) True if all tests pass, otherwise False. If path doesn not exist, returns False. 

---

<!-- TOC ignore:true -->
## py_unittests_number

> Checks how many unit tests were run.

*Parameters:*

* **path** (`str`): Path to the test file or directory with tests relative to the student github folder
* **options** (`str = ""`): Bash variables to declare before running the tests

*Returns:*

* (`int`) Amount of unit tests that were run. 

---

<!-- TOC ignore:true -->
## doctest_number_passed

> Checks how many doctests passed.

*Parameters:*

* **path** (`str`): Path to the test file
* **options** (`Optional[list[str]] = None`): Options to pass to doctest

*Returns:*

* (`int`) Amount of doctests that passed. 

---

<!-- TOC ignore:true -->
## doctest_number_failed

> Checks how many doctests failed.

*Parameters:*

* **path** (`str`): Path to the test file
* **options** (`Optional[list[str]] = None`): Options to pass to doctest

*Returns:*

* (`int`) Amount of doctests that failed. 

---

<!-- TOC ignore:true -->
## pycodestyle

> Verifies that files are following pycodestyle format.

*Parameters:*

* **paths** (`list[str]`): Paths to files to be checked
* **options** (`Optional[list[str]] = None`): Options to be passed to pycodestyle

*Returns:*

* (`bool`) True if all files follow pycodestyle format, otherwise False 

---

<!-- TOC ignore:true -->
## shellcheck

> Verifies that files are following shellcheck format.

*Parameters:*

* **paths** (`list[str]`): Paths to files to be checked
* **options** (`Optional[list[str]] = None`): Options to be passed to pycodestyle

*Returns:*

* (`bool`) True if all files follow shellcheck format, otherwise False 

---

<!-- TOC ignore:true -->
## betty_doc

> Verifies that files are following betty-doc format.

*Parameters:*

* **paths** (`list[str]`): Paths to files to be checked
* **options** (`Optional[list[str]] = None`): Options to be passed to betty-doc

*Returns:*

* (`bool`) True if all files follow betty-doc format, otherwise False 

---

<!-- TOC ignore:true -->
## betty_code

> Verifies that files are following betty-style format.

*Parameters:*

* **paths** (`list[str]`): Paths to files to be checked
* **options** (`Optional[list[str]] = None`): Options to be passed to betty-style

*Returns:*

* (`bool`) True if all files follow betty-style format, otherwise False 

---

<!-- TOC ignore:true -->
## w3c

> Runs w3c validation on html files.

*Parameters:*

* **paths** (`list[str]`): List of paths to the html files relative to the student github folder

*Returns:*

* (`bool`) True if all files are valid, otherwise False 

---

<!-- TOC ignore:true -->
## nasm

> Checks that ASM files can be compiled successfully.

*Parameters:*

* **paths** (`list[str]`): List of file paths relative to the student github folder or to the checker correction repository
* **options** (`str = ""`): Options to pass to the nasm command
* **timeout** (`int = 30`): Deadline for the command in seconds

*Returns:*

* (`bool`) True if the nasm command executes successfully, otherwise False 

---

<!-- TOC ignore:true -->
## git_change_branch

> Changes the git branch of the student repository.

*Parameters:*

* **branch_name** (`str`): Name of the git branch

*Returns:*

* (`bool`) True if the branch changed successfully, otherwise False 

---

<!-- TOC ignore:true -->
## git_reset

> Discards all changes and reverts student github repository to the last commit.

*Returns:*

* (`bool`) True if the command was successful, otherwise False 

---

<!-- TOC ignore:true -->
## git_commit_id_by_message

> Returns the commit id that contains the given message

*Parameters:*

* **message** (`str`): String to search for in the commit messages

*Returns:*

* (`str`) Commit id that includes the given message. If no commit is found, will return an empty string 

---

<!-- TOC ignore:true -->
## http_get

> Gets content from the given URL (follows the redirects).

*Parameters:*

* **url** (`str`): URL to get content from
* **auth_username** (`Optional[str] = None`): Basic authentication username
* **auth_password** (`Optional[str] = None`): Basic authentication password
* **timeout** (`int = 10`): Deadline for the request to complete

*Returns:*

* (`str`) Content of the given URL if the request was successful, otherwise empty string 

---

# Docker images

To build a Docker image, run the following command from the root of the
repository:
```
./build_docker_image.sh
```

Without arguments this will build the `default` Docker image that contains tools
for most of the corrections. The Docker image will have name
`checker-worker:latest`.

If you need more setup in the Docker image, such as NodeJS packages, you can use
other images like `nodejs-redis`:

```
./build_docker_image.sh nodejs-redis
```
This will build the Docker image `checker-worker-nodejs-redis:latest`. 

Note that all other Docker images depend on the `default` one, so if you change
it, you must also rebuild other images. If you want to update the
`corrections_hbtn` repository, you would need to specify `--no-cache` in the
command above.

To build all Docker images, run:

```
./build_docker_image.sh all
```

# Checker v1 to Checker v2

Note that Checker v2 supports more functions, so not all Checker v2 functions
are listed here for the mapping. Please check the section above.

You don't need to use `absolute_student_path` anymore as all student files are
specified relative to the student github folder and are resolved automatically.

## Translate single command

To translate a single command from Checker v1 to Checker v2, you can use the
following script:
```
python3 ruby_to_python.py -c 'files_exist(["file1"])'
```

## Translate commands from CSV

To translate multiple commands, you can create a CSV file with the following
format:

```
124169,"files_exist([""0-lockboxes.py""])"
122145,"files_exist([""0-insert_number.c""])"
```

File should consist of 2 columns, check id and the ruby command, without the
header. Then you can run the following command to translate Checker v1 command
to Checker v2:

```
python3 ruby_to_python.py -f commands_in.csv
```

It will generate 3 files:
* `commands_out.csv`: Checker v2 commands that were successfully translated, in
  the same format as the input file.
* `commands_invalid.csv`: Checker v1 commands that could not be parsed, usually
  due to a missing or extra brackets.
* `commands_not_supported.csv`: Checker v1 commands that are not yet supported.


## Function mapping

Native operators: 

| Checker v1   | Python operator   |
|:-------------|:------------------|
| `is_equal`   | `==`              |
| `op_add`     | `+`               |
| `op_sub`     | `-`               |
| `op_mult`    | `*`               |
| `op_mod`     | `%`               |
| `op_and`     | `and`             |
| `op_or`      | `or`              |
| `op_lt`      | `<`               |
| `op_le`      | `<=`              |
| `op_gt`      | `>`               |
| `op_ge`      | `>=`              |
| `op_not`     | `not`             |
| `is_null`    | `not`             |

 --- 

Checker functions (highlighted have different name):

| Checker v1                   | Checker v2                            |
|:-----------------------------|:--------------------------------------|
| **_`to_integer_value`_**     | **_`lazy_int`_**                      |
| **_`number_occurrences`_**   | **_`number_of_occurrences`_**         |
| `folders_exist`              | `folders_exist`                       |
| `files_exist`                | `files_exist`                         |
| `files_empty`                | `files_empty`                         |
| `copy_files`                 | `copy_files`                          |
| **_`copy_container_files`_** | **_`copy_files`_**                    |
| `copy_and_replace_file`      | `copy_and_replace_file`               |
| **_`number_lines`_**         | **_`number_of_lines`_**               |
| `valid_number_of_lines`      | `valid_number_of_lines`               |
| `compare_preload`            | `compare_preload`                     |
| `compare`                    | `compare`                             |
| `malloc`                     | `malloc`                              |
| `make`                       | `make`                                |
| **_`preproc_contains`_**     | **_`preprocessed_does_not_contain`_** |
| `contains`                   | `contains`                            |
| `file_contains`              | `file_contains`                       |
| `file_contains_regex`        | `file_contains_regex`                 |
| **_`words_not_allowed`_**    | **_`file_does_not_contain`_**         |
| `file_content`               | `file_content`                        |
| `exec_bash`                  | `exec_bash`                           |
| **_`dry_exec_bash`_**        | **_`exec_bash_ignore_errors`_**       |
| **_`execution_success`_**    | **_`exec_bash_success`_**             |
| **_`run_bash`_**             | **_`exec_bash_compare`_**             |
| **_`sandbox_valid`_**        | **_`container_valid`_**               |
| **_`remote_exec`_**          | **_`container_exec_bash`_**           |
| `sass_compile`               | `sass_compile`                        |
| `gcc`                        | `gcc`                                 |
| `valgrind_leak`              | `valgrind_leak`                       |
| `valgrind_error`             | `valgrind_error`                      |
| **_`count_allocations`_**    | **_`valgrind_allocations`_**          |
| **_`ltrace`_**               | **_`ltrace_allowed`_**                |
| **_`ltrace_not`_**           | **_`ltrace_not_allowed`_**            |
| **_`count_calls`_**          | **_`ltrace_count`_**                  |
| `semistandard`               | `semistandard`                        |
| `node_lint`                  | `node_lint`                           |
| `py_unittests`               | `py_unittests`                        |
| `py_unittests_number`        | `py_unittests_number`                 |
| `doctest_number_passed`      | `doctest_number_passed`               |
| `doctest_number_failed`      | `doctest_number_failed`               |
| **_`pep8`_**                 | **_`pycodestyle`_**                   |
| `pycodestyle`                | `pycodestyle`                         |
| **_`shellchecker`_**         | **_`shellcheck`_**                    |
| `betty_doc`                  | `betty_doc`                           |
| `betty_code`                 | `betty_code`                          |
| `w3c`                        | `w3c`                                 |
| `nasm`                       | `nasm`                                |
| `git_change_branch`          | `git_change_branch`                   |
| `git_reset`                  | `git_reset`                           |
| `git_commit_id_by_message`   | `git_commit_id_by_message`            |
| `http_get`                   | `http_get`                            |
