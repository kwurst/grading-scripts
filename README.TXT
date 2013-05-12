Scripts for grading student programs.

The student programs are pulled from remote git repositories. 
These scripts produce PDFs for grading, and return them to student repos after grading. 
Graded files are pushed back to remotes.

Planned Workflow:

A. Pull all from remote repositories

B. For each student:
    1. Switch to student's branch
    2. Convert program files to a single PDF (convert and append)
    3. Put PDF in grading folder (grading/student/assignment/file.pdf)

C. Grade PDFs on iPad

D. For each student:
    1. Switch to student'sbranch
    2. Copy PDF to correct folder (assignment/file.pdf)

E. Push all to remote repositories
