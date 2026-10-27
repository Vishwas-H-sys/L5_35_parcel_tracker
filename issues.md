Lab 5: Static Code Analysis — Issues and Fixes

Program: parcel_tracker.py

Issue Documentation

Issue	Type	Line(s)	Description	Fix Approach
Mutable Default Argument	Bug	Verify from Pylint report	The bookParcel() function uses history=[] as a default argument. The same list can be shared across multiple calls.	Change the default to None and create a new list inside the function when needed.
Broad Exception Handling	Code Quality	Verify from Pylint report	trackParcel() catches a general Exception, which may hide unexpected errors.	Catch KeyError specifically when the tracking ID does not exist.
Insecure Temporary File Creation	Security	Verify from Bandit report	tempfile.mktemp() can introduce a race condition because the filename is generated without securely creating the file.	Use tempfile.NamedTemporaryFile() or another secure temporary-file API.
Subprocess Command Execution	Security	Verify from Bandit report	The pingHub() function invokes a subprocess. Unsafe command construction can expose the program to command injection.	Pass arguments as a list, keep shell=False, validate input, and use a timeout.
Partial Executable Path	Security Review	Verify from Bandit report	Using "ping" relies on the system’s executable search path.	Resolve the executable using shutil.which() and handle cases where it is unavailable.
Inconsistent Formatting	Style	Verify from Flake8 report	Inconsistent spacing around operators and function calls makes code harder to read.	Follow PEP 8 formatting and rerun Flake8.

Verification

After applying fixes, the program was checked using:

* Pylint for code quality.
* Bandit for security-related findings.
* Flake8 for formatting and style.

The final reports should be reviewed to confirm that the issues have been resolved or appropriately documented.