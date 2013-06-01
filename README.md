Scripts for grading student programs.

The student programs are pulled from remote git repositories. 
These scripts produce PDFs for grading, and return them to student repos after grading. 
Graded files are pushed back to remotes.

Planned Workflow:

1. Pull all from remote repositories

2. For each student:

	1. Switch to student's branch
	2.  Convert program files to a single PDF (convert and append)
	3. Put PDF in grading folder (grading/student/assignment/file.pdf)

3. Grade PDFs on iPad

4. For each student:

	1. Switch to student'sbranch
	2. Copy PDF to correct folder (assignment/file.pdf)
	3. Copy assignment solution to correct folder

5. Push all to remote repositories
