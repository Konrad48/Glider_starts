# Risk in glider take-offs
#### Video Demo:  https://youtu.be/Yky1hlz4Aqs
#### Introduction:
Writing this program was a part of my master’s thesis titled “Human factor’s influence in safety of glider take offs”. Thesis is written in polish language, so if you are familiar with it feel free to message me for the source! It was also submitted as my final project in CS50 Course.
#### Description:
Main goal of the project was to build a model for estimating risk in glider take offs. This program’s purpose is to simulate events according to drawn trees of events. It’s a command line program written in Python.
Tree of events shows all the possible paths of event that occur after the initiating event marked as A(j) where j is it’s unique number. 6 trees were created for the thesis and can be found in the repository.

Reaction times of pilot, flight director, tow pilot and winch operator were modeled as random variables and characterized by Weibull distribution. Weibull distribution is similar to Normal distribution but additional parameters make it much more flexible. Three levels of experience were considered in the model, for each one different parameters of Weibull distribution were used. Each time variable has it’s mean time, estimated by an expert. Additionally in the A(1) event, other distributions: Uniform, Exponential and Normal were tested and are possible to set.
#### Time variables:
-	tp1 – Gilder pilot’s 1st reaction time
-	tp2 - Glider pilot’s 2nd reaction time
-	tk – Flight director’s reaction time
-	th – Tow pilot’s reaction time
-	tw – Winch operator reaction time

Event trees are in the folder in form of pictures. On each branch there is a condition(s) that must be valid for certain path to occur or there are probabilities of certain events.
Program runs, a given number of simulations generating random reaction times and events according to distributions. Then it returns a list of probabilities via print method except for events  A(2) and A(4). For these two events, program creates a .csv file with probabilities and dangers in function of height./
#### Usage:
Required packages can be found in requirements.txt

It can be launched using command line and takes 3 to 4 arguments:
1.	Initial event number (1-6)
2.	Experience level (0-2) where 0 - unexperienced pilot before license exam, 1 – pilot after exam but with < 350 hours of flying, 2 experienced pilot with > 350 hours of flying
3.	Number of events to be simulated, with increasing the number the accuracy increases but also program’s running time
4.	Optional parameter for changing Tp1 distribution in A(1): 1 - Weibull distribution, 2 - Uniform distribution, 3 – Exponential distribution, 4 – Normal distribution

python probab1.py initial event nr., experience level (0-2), no. simulations, distribution in A(1) (optional)

#### Example:
python probab1.py 1 0 100000 1
