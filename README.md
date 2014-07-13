Scripts for preparing student programs for grading.

Scripts convert student repository code to a PDF file for
grading.

## Example

In this example we have the following structure:

    hw1
    ├── config.json
    └── submissions
        ├── jh
        │   └── Lab10Code
        │       ├── Employee.java
        │       ├── Faculty.java
        │       ├── Person.java
        │       ├── Staff.java
        │       └── Student.java
        └── wk
            └── Lab10Code
                ├── Employee.java
                ├── Faculty.java
                ├── Person.java
                ├── Staff.java
                └── Student.java


`config.json` contains the following:

    {
	"directory" : "/Users/karl/GoogleDrive/Courses/CS-140/StudentSubmissions/S1-2014/grading/Lab10",
	"files" : [
		"Lab10Code/Person.java",
		"Lab10Code/Student.java",
		"Lab10Code/Employee.java",
		"Lab10Code/Faculty.java",
		"Lab10Code/Staff.java"
	]
    }

* `directory` - Path to the directory containing student submission
  subdirectories. Paths are relative to the configuration file's location.
* `files` - List of files to process for each submission directory. Paths are
  relative to each student's submission directory.

`submissions` contians a subdirectory for each students' work. The names of each
subdirectories is not important. In this example they are the initials of each
student.

We process the assignment as follows:

    $ python path/to/assignmentconvert.py hw1/config.json

## Run tests

    $ cd grading-scripts
    $ python run_tests.py

## Writting a processor

See `assignmentconvert.py` for an example.
