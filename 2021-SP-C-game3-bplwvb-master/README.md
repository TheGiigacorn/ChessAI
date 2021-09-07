#################################
#	Coding Standards	#
#################################

You can use any of the following programming languages for your submission : 
	- C++
	- C#
	- Java
	- Python3 (NOT Python2)
Your code must be well formatted and styled according to good coding standards, such as the MST coding standard outlined here : 
http://web.mst.edu/~cpp/cpp_coding_standard_v1_1.pdf
It is required that your code is well documented.

NOTE : Sloppy, undocumented, or otherwise unreadable code will be penalized for not following good coding standards (as laid out in the grading rubric on the assignment document) 


#################################
#          !IMPORTANT!          #
#################################

* Read the `README` in the sub-directory corresponding to your chosen language.  

* Read the chess framework's documentation for your chosen language here : http://docs.siggame.io/chess/ 

#################################
#	Submission Rules	#
#################################

Included in the top level of your repository is a file named `readyToSubmit.txt`. When your program is ready to submit, change the first line of this file to the word `yes` or `Yes` and the second line to your chosen programming language. 
You may commit and push as much as you want, but your submission will be graded unless the first line of `readyToSubmit.txt` is `yes`. If you do not plan to submit before the deadline, then you should NOT modify `readyToSubmit.txt` until your final submission is ready. Once your final submission is ready, change the first line of `readyToSubmit.txt` to `yes`.

#################################
#       Compiling & Running	#
#################################

You have been provided a bash script called `play.sh`, which compiles and runs your code; it also starts a game session between your AI and itself. DO NOT MODIFY THIS SCRIPT.
You can run `play.sh` using the following command format :

	./play.sh Joueur.<lang> Session_ID

Where `Joueur.<lang>` is the directory for the language you are coding in. An example of the above command for c++ would be :

	./play.sh Joueur.cpp AIisAwesome
