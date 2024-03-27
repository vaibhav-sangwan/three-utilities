What is this?
=============

Three Utilities is a mathematical puzzle game for the Sugar desktop.

![alt text](https://github.com/vaibhav-sangwan/three-utilities/blob/main/screenshots/try_3.png?raw=true)

There are 3 houses in a town and 3 utilities - water, gas and electricity for which you have to lay down supply lines for. The supply lines must not intersect with each other. Click on any of the utilities to start laying down the pipelines and click on a house to terminate the pipeline. Find a solution such that all houses are connected with all 3 utilities.


How to use?
===========

Three Utilities can be run on the Sugar desktop.  Please refer to;

* [How to Get Sugar on sugarlabs.org](https://sugarlabs.org/),
* [How to use Sugar](https://help.sugarlabs.org/)

How to run?
=================

Dependencies:- 
- Python >= 3.10
- PyGObject >= 3.42
- PyGame >= 2.5
  
These dependencies need to be manually installed on Debian, Ubuntu and Fedora distributions.


**Running outside Sugar**


- Install the dependencies

- Clone the repo and run -
```
git clone https://github.com/vaibhav-sangwan/three-utilities.git
cd three-utilities
python main.py
```

**Running inside Sugar**

- Open Terminal activity and change to the Three Utilities activity directory
```
cd activities\ThreeUtilities.activity
```
- To run
```
sugar-activity3 .
```