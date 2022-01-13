# EEN150 Intelligent Automation: The predicate hand-in

This is the first python programming hand-in in the course where you will learn some basics in python programming practices, like using virtual environment and tests, as well as how to create data structures to be able to compute some simple search algorithms. The main components are state, predicates, actions, transitions and graphs.

The hand-in is divided into five tasks:

- state
- guards
- actions
- transition
- graph

You will solve each task by implementing code so that the included tests passes. Continuously you will also push your code to github and your repository, where it will be tested automatically.


## Installation

Start by reading the three first parts in https://dev.to/codemouse92/introducing-dead-simple-python-563o. This is a really good tutorial so try to read all parts when you have time.

Below are the basic instructions to install the required tools. There will however be extra instructions in a FAQ on canvas based on issues we discover. So also go and check the FAQ in the the discussions.

Then:

- Install python 3.9
    - Follow the instruction Getting the Tools on this page: https://dev.to/codemouse92/dead-simple-python-virtual-environments-and-pip-5b56
    - It is important that you have installed 3.9 since some new features are used that may requirer it.
    - check that the installation works by running in a terminal. Depending on your installation you may have to use either python, python3 or python3.9 

```console
python --version
# or 
python3 --version
# or
python3.9 --version
# or
py --version
```


- Install visual studio code (VSC). 
    - https://code.visualstudio.com/docs/setup/setup-overview
    - Install the python extension. You will find it under the extension tab on the left inside VSC when you search for python. It is the extension from microsoft: https://code.visualstudio.com/docs/languages/python
    - You can use any IDE, for example like pyCharm, but i suggest to use VSC since all instructions are based on that
    - There are a lot of good tutorials for VSC on youtube, for example https://youtu.be/7EXd4_ttIuw
    - If you already have VSC installed on your computer, check so that it is the latest version (The button "check for updates" inside VSC did not work for me on windows, so download the latest and reinstall if you have an old version)

- clone this repository to your computer
    - The simplest way is to use github desktop https://desktop.github.com. But calling git clone from a terminal also works. VSC also have built in git support (https://code.visualstudio.com/docs/editor/versioncontrol)
    - A great video about git and github here: https://youtu.be/DVRQoVRzMIY
    - Learn more here: https://docs.github.com/en/get-started/quickstart/set-up-git
    - and more about git: https://docs.github.com/en/get-started/quickstart
    - Important: Do not just download the repository as a zip-file, clone it
    - When you are working with the tasks, commit your changes and push to github so you do not loose anything
    

- Open a terminal and cd into the assignment folder. In that folder write
```console
python -m venv venv
# or python3 or python3.9 or py
```

If you have Mac or Linux, write
```console
source venv/bin/activate
```

or if you have windows :
```console
venv\Scripts\activate.bat
```

Now, you are inside the virtual environment, which you can see in the console since it starts with 
```console
(venv)
```

When you are inside the virtual environment, you can install the required dependencies
```console
(venv) pip install -r requirements.txt 
```
If you get an error while installing, just try to run the same command again.

and finally start visual studio code: 
```console
(venv) code ./
```
You can also start VSC when you are not inside the venv, as long as you start it in the assignment folder, it will find the venv. It is also possible to open the folder inside VSC.

To leave venv, just type
```console
(venv) > deactivate
```


## Introduction

This assignment is in part, a way to learn how to implement good data structures in python that are relevant for this course, like states, predicates, transitions and graphs. But another important learning outcome is that you will learn how to develop real programs using the tools and methods we use in industry. So a large part of the challenges in this assignment is to start learning git, develop code using unit tests, structure your python code in ways that are easy for others to reuse, and to learn modern python features like type hints, comprehensions, dataclasses, docstrings and other fun stuff. 

There will probably also be problems when installing all these tools and libraries. When working as engineer, trying to solve installation problems are extremely common and frustrating, so it is good to learn how to deal with it in an organized way. The key technique you have to learn is to google the error message, or ask around, or ask us teachers. 

During this assignment, you have to read all comments in the files and the code. In some comments, there will be links to more information about all these concepts so you learn as you dive into the code.

If you get a lot of errors when you open the repository for the first time and nothing works, check so that you are running python 3.9 at the bottom of VSC. It can also be that you have not installed the requirements inside the virtual environment venv. Try to repeat the steps above or ask someone to help you out. 

### Some getting starting information

Throughout the code, I have added links to more information about various concepts related to python programming. It is important to check those to better understand what is going on in the code. I have also found some good links about more general concepts:

The main concept that we will be using while developing code, is test-driven development. The idea is that you always write a test function for all your "program" functions that you write. This is especially important when developing python code. Here is a really good introduction to unit testing in VSC and python: https://youtu.be/UMgxJvozR5A. 20 minutes into the video, he is using the built in testing framework in VSC that you will be using.

Another good video is this about common mistakes when programming python: https://youtu.be/fMRzuwlqfzs

If you feel that you need to refresh your python knowledge, or if it is a new language, I recommend this online resource: https://www.programiz.com/python-programming, but there are also many more. One important comment though, that online resource as well as many others are not using type hints, tests or dataclasses. This is not necessary in python, but is a good practice, which is why we use it in this course.


## Task 1

In the first task we will create a class that will represent states, where a state stores a number of variables and their current values. The two important files that you can open are

/predicates/state.py

and 

/predicates/tests/test_states.py

In this assignment I have been using type hints to support the user of the code. You can read more about type hints here: https://docs.python.org/3/library/typing.html, as well as dataclasses, which is described in some links in the state.py file. Some pros and cons about type hints: https://youtu.be/QS7m167SVXU

Start first by looking though the state.py and try to understand the state class. After that go to the test_states.py and run the tests. In VSC you can run all tests by pressing the test beaker icon and then press play. You can also run the tests from the command line, by running the command pytest when you are in venv.

The 3 first tests in test_states.py will pass and be green. Your task is now to make the the tests test_state_getting_values(), test_next_state() and test_next_state_immutable() to also be ok by implementing the functionality of the 2 functions:

```python
def get(self, key: str) -> Any:
```

```python
def next(self, **kwargs) -> State:
```

You can see where you need to update the code by the finding and removing

```python
raise NotImplementedError
```

The state class is a wrapper around a dictionary. More about dicts: https://www.programiz.com/python-programming/dictionary. In this code, it would have been possible to just use the dict datatype to represent a state. The benefit of wrapping it inside a class is that then we can add new methods as well as guarantee that the state is not changed when it is created. Later on, we will also store states in the sets, which requirer that each item is hashable. The hash of an object is an integer number that can be used to quickly find if two objects are equal. Read more about it here: https://eng.lyft.com/hashing-and-equality-in-python-2ea8c738fb9d

tip of the day: if you add a print(...) inside a test, you can only see that if the test fails. When it fail, you will se it under output, and choose python Test Log in the dropdown list (https://code.visualstudio.com/docs/python/testing)

tip of the day 2: Tests are not only used for checking if your code works. It is also a good way to show some examples how to use your code

tip of the day 3: If you want to test some of your code without using the tests, check the files __main__.py in predicate and graph. There you can write code and run it.


## Task 2

When you have the State class fully functional, now it is time to commit your changes and push the commit to github. Either you do it directly in VSC, in github desktop or via the terminal. When you have pushed the code, all tests will also run online. However, in this assignment these tests will be the same as you already have in your repository.

In this second task, you will implement the missing functionality of the guard predicates. The tests are in 

predicates/tests/test_guards.py

and the implementations are in 

predicates/guards.py

The first class in this file is:

```python
class Guard(Protocol):
```

You do not really have to understand this class, but can read more about Protocols by following the links in the docstring of the class. We are using this class so we later can use Guard as a type hint for all our different guard classes

A guard is a predicate over a state, which either evaluates to True or false, based on the current values of the variables in that state. Each guard implements the function:

```python
def eval(self, state: State) -> bool:
```

that given a state should return if the guard is true.

To be able to write various guards, we need to have a data structure where we can store predicates like (v1 == "open") && !v2, where && is AND and ! is not. In this assignment, we will implement the following: Eq, Beq, Not, And and Or. 

You task in this assignment is to implement the eval functions for these guards. The Beq, which is a boolean equal that we use for variables that are either true or false, is already implemented, but the rest is left for your.

At the end of the guards.py file, there is a parser already implemented. This parser makes it easier for us to write down guards as text. If you are interested, you can take a look, but you will mainly use it later in the course. You can see in the tests how the parser is used.


## Task 3

Ok, great work to implement the guards. If you haven't done some yet, commit and push your solution. It is actually preferred to commit changes frequently so you do not loose anything. If you want to revert some changes or go back, that is easy in git:

https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/managing-commits/reverting-a-commit
https://medium.com/swlh/using-git-how-to-go-back-to-a-previous-commit-8579ccc8180f

Now it is also time to try out working with branches. So for this task, create a branch and commit your changes to this new branch. When the task works, merge your branch with the master branch. If you want, you can try to do what github calls a pull request. If you get conflicts, then resolve them and commit the fixed files. This can feel tricky, but try to experiment and learn how to resolve conflicts by creating yet another branch, change the same part of the code in both branches, but in different ways (for example add a comment somewhere). Commit the changes in both branches, and try to merge the commits from one branch to the other. Some more info:

https://code.visualstudio.com/docs/editor/versioncontrol#_branches-and-tags

https://code.visualstudio.com/docs/editor/versioncontrol#_merge-conflicts

https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/making-changes-in-a-branch/managing-branches

pull requests: https://docs.github.com/en/github/collaborating-with-pull-requests
There is also a github plugin for VSC: https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github, if you would like to work with pull requests.

If both of you in the pair would like to work at the same time, try to use different branches. 

So time to go back to some more coding. In this task you will implement the actions and the files are predicates/tests/test_actions.py and predicates/actions.py. The task is to implement the:

```python
def next(self, state: State) -> State:
```
for all the action classes. This function takes a state and creates a new state with the updated variables based on the action. Read the tests and the docstrings in the classes to figure out what each action class should do. Also the actions have a parser in the end of the file, but nothing you need to change.

When you are done with this task, merge your branch with the master branch and push to github.

## Task 4

Now we are done with the state, guards and actions. It is time to implement the transition. The tests are located in graphs/tests/test_transition.py, and the code should be implemented in graphs/transition.py

I planned to remove the transition class all together, but then the tests didn't work for the other parts, so you will get the first part of the class. There may still be some instruction telling you to create the class. 

A transition consists of a guard and a list of actions. To be able to use the transition, you should implement the eval and next methods. Check the tests to better know how each method should behave. 


## Task 5

And commit and push your progress as always

No we are at the final task, which is the most fun and interesting part. The previsou tasks was just to build the components that we will use to build graphs. 

The tests are in graphs/tests/test_graph.py and the files where you will implement are graphs/factory.py and graphs/graph.py.

A graph is a data structure that includes edges and vertices. The graph do not know anything about transitions or states. So to later analyse a system, we would like to create a graph based on a set of transitions and an initial state. To do this, you should implement an algorithm in the factory.py:

```python
def graph_factory(state: State, transitions: List[Transition]) -> Graph:
````

In this algorithm you need to create the parts that your graph requirers by searching through a reachable states by firing transitions. How you would like to represent the graph inside the graph class is up to you, but a simple way is just to store all edges in the class. Maybe not so efficient though, but good enough for now.

The factory method could be implemented using recursion or a while loop and a stack / list. I suggest that you use a while loop. Start with the initial state, check what transitions that are enabled, create the next states by calling next on the enabled transitions, add the new states to the a stack / list, create the edges and save them, and then contribute iterate until there are no more states in the stack / list. Observe that you only should create edges for the same state once, else you will end up in an infinity loop. We will talk more about this in the lectures...

When implementing this method, it could be useful to run the tests in debug mode. In for example the factory.py, add a pause sign by clicking to the left of the line number so a red dot appears. No right-click on the small circle to the left of the test test_make_me_a_graph() and select debug test. Now the code will stop executing at the pause sign and you can execute line by line and also see what the variables currently are.

In the graph.py, I have already created a class for  Edge and one class for Vertex. Use the from_state methods when creating these so that the names will be the same as in my tests.

The rest of the tests checks that you have implemented all the methods in the graph class. Check the tests and the descriptions in the class.

When you are done with this task, all tests should pass and you can commit and push the final solution to github! 

The things you have learned in this assignment will be reused in the next assignment where you will implement simple search algorithms in a graph-like structure. This will we then use to find a plan for two robots to sort cubes.


