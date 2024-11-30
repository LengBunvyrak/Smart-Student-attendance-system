This is my project for computer Science A class. 
Instruction of how to run to software:
First you need to install some necessary libraries such as:  

Opencv - pip install opencv-contrib-python

Numpy - pip install numpy

Face-recognition - pip install face_recognition

Pillow - pip install pillow 

First we need to install all the necessary library, then we can use IDE such as VScoode or Pycharm. Then open the main.py file and run it.


1. Project Title : Flying Chicken - Smart Student Attendance System


2. Project issue, problem to be solved
		The aim of this project is to address the problem with the traditional attendance system where it could be digitalized to improve time efficiency so that class time can be utilized more. It also help to solved the problem of impersonation where students might fake attendance for their friends. With this solution it will improves efficient and reliable record-keeping. 


3. Current progress 
		-Ideation: I want to create a face recognition system that can detect the face of students and from the recognition we will note it down. 
		-Planning: I did some research around OpenCV and search for youtube tutorial on how to work with opencv and start following a few of the students attendance system projects. 
		-Implementation: The project partly follow the youtube tutorial for the part of student face recognition and how to implement face recognition. After that I built a GUI so that it would be easier for user navigation and easier accessibility to the function.
		-Deployment: after some testing and adjustment to fixing the error, I can firmly say the project is working how I would like it to be. 



4. Project Functions/Features
-Student face registration: for this function, the main goal is to be able to register student information into the database so that we can use it for the recognition stage. The information that we take in would be the id, name and capture a picture of them so that we can save it for face recognition. 
-Student Attendance System: After we have the faces of the student stored in a directory within the program folder, we can initiate the student attendance system, it take the face from the face directory and the face_recognition library we handle all the process of encoding and processing and in return giving us the output of who is presented and time and date will also be noted down. 


5. Expected No. of Pages 	
There are 3 pages to this program which consist of:
Home page for the options of function
Student face registration page
Student attendance system page


6. Database applied
		- For this project, I used sqlite3 as the database that would store the table of student name, id, major, time and date for the attendance, and the status of their attendance. 


7. Project reference/source (Youtube, tutorial web, etc...)
	https://youtu.be/oXlwWbU8l2o?si=x1Idk1a_V913ou_F
	https://www.youtube.com/watch?v=iBomaK2ARyI&t=2531s
https://youtu.be/vHuM6hkHMxE?si=5ZRpRHRHyi2rwc6S
