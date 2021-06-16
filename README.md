## Table of contents
* [Abstract](#abstract)
* [Modules](#modules)
* [Problem](#problem)
* [Objective](#objective)
* [Setup](#setup)

## Abstract
We propose a ‘E-HealthCard’ which contains a unique identifier which is
used to index into a globally available database housing the medical history
of the holder. This will be especially useful in rural and impoverished areas
where a person seeking medical attention may or may not have information
(or complete information) of the previous treatments he/she has had. It
will provide the necessary personnel with the necessary information about a
patient’s medical history in order to treat him/her better.
	
## Modules
Our system has four major modules.:
* Patient
* Doctor
* Paramedics


## Problem
No globally available database housing medical history of a patient. Most
solutions are limited to a single entity. Not having the proper information
about the medical history of the patient usually slows down treatment.

## Objective
To provide the necessary personnel with the necessary information about a
patient’s medical history in order to treat him/her better.

## Setup
To run this project:

```
$ git clone https://github.com/sagarbgohil/E-HealthCard.git
$ cd EHealthCard
$ pip3 install -r requirements.txt
$ py manage.py runserver
```