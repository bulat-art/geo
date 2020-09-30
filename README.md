# geo
REST-API with Geoname
# Task for Infotecs(Analyst (python))
## Getting Started
File: RU.txt from http://download.geonames.org/export/dump/RU.zip \\
Programming language: Python 3
Installed libraries pandas 1.1.1 and flask 1.1.2
Run script.py and after that server running on *http://127.0.0.1:8000/*
## Description
### 1st method
Input value into the form *1method. geonameid* and click "1".
You will see information about the city in HTML table. If you do something wrong, the program will notify you about it.
### 2nd method
Input values into the forms *Page*,*Count* and click "2".
You will see a page=*Page* from the book with the number=*Count* of cities on it.
### 3hd method
Input values into the forms *First city*,*Second city* and click "3". 
You will see information about First city and Second city in HTML table. Also there will be information about timezones and which city is North. If several cities have the same name, the program will select the one with the largest population.
### 4th method
Input values into the forms *Beginning*,*name or altname* - where you want to search the beginning of the name and then click "4".
You will see the list with cities which start with *Beginning*. 
This list will be sorted by population.
##### Authors
- Yakupov Bulat
