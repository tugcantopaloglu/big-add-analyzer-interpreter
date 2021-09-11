# Lexical Analyzer and Interpreter for Big Add Language
**Design and Problem Analysis**  
The challenge at hand is one of code analysis and execution. We must examine an input file whose name is provided by the user. We have a custom language called "Big Add Language" that features classic declarations and basic addition, subtraction, assignment, loop, and code block conditions in this special situation. Lexical Analyzer takes a code file analysis file and feeds it to the interpreter with declarations, errors, comments, data types, and assignments. When the analyzer detects an error, it will send it to the interpreter, who will display it to the programmer before terminating the code.  
Every line in the input file will be analyzed by the interpreter, and the file will be executed using the tokens provided. To begin, the interpreter will look for the first token. If the analyzer finds a token that is legitimate, the interpreter will add it to the stack and utilise it for the calculations that are expected. If the interpreter cannot detect a token on a line, it will ignore whitespace and comments when searching for another line. As a result, if the analyzer finds a comment, it will take it out of the code because comments do not run in the compiler. If the analyzer comes across a loop or a calculation, it will identify it as a loop or a calculation. This will be done by the analyzer for each line before passing them on to the interpreter. If it detects an error, it will terminate the code and display the results to the programmer.  

**Code Tests**  
Code was written in the C programming language, developed in Code Blocks 20.03 and compiled with the standard Code Blocks compiler.  

**Test-1**  
![test1](https://user-images.githubusercontent.com/53763911/132947968-2cd81500-f986-49b0-9a29-7c7b6096be9d.PNG)  

**Test-1 Output**  
![test1-end](https://user-images.githubusercontent.com/53763911/132947983-66153437-fc85-45f1-a611-7b7ec7ba3d1b.PNG)  

**Test-2**  
![test2](https://user-images.githubusercontent.com/53763911/132947991-12aa86ec-aba3-46e2-ab6e-e33d92e1af6e.PNG)  

**Test-2 Output**  
![test2-end](https://user-images.githubusercontent.com/53763911/132948003-aa3b1267-a8ec-4ede-85d1-8f40c55a6931.PNG)  

**Test-3**  
![test3](https://user-images.githubusercontent.com/53763911/132948014-e02a9ba0-a51e-481c-b2d7-7a74efd7d931.PNG)  

**Test-3 Output**  
![test3-end](https://user-images.githubusercontent.com/53763911/132948023-264840d6-c4e6-4755-a945-735db6ecc08b.PNG)  

**Test-4**  
![test4](https://user-images.githubusercontent.com/53763911/132948028-81f70136-e6fc-46e7-ab45-208839b18534.PNG)  

**Test-4 Output**  
![test4-end](https://user-images.githubusercontent.com/53763911/132948040-5eff5838-9444-4a6e-8e1d-ed9920ea5525.PNG)  
