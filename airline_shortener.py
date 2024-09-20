# -*- coding: utf-8 -*-

def shorten_airline(airline_name):

    if airline_name == "lufthansa (deutsche lufthansa ag)":
        airline_name = "lufthansa"

    if airline_name == "iberia lineas aereas de espana":
        airline_name = "iberia"

    if airline_name == "swiss international air lines":
        airline_name = "swiss"

    if airline_name == "sas scandinavian airlines":
        airline_name = "sas"

    if airline_name == "klm royal dutch airlines":
        airline_name = "klm"

    if airline_name == "wideroe flyveselskap a/s":
        airline_name = "wideroe"

    if airline_name == "air europa líneas aéreas":
        airline_name = 'air europa'

    if airline_name == "corendon airlines europe":
        airline_name = "corendon"

    if airline_name == "swiss global air lines":
        airline_name = "swiss"

    if airline_name == "norwegian air shuttle":
        airline_name = "norwegian"

    if airline_name == "condor flugdienst":
        airline_name = "condor"

    if airline_name == "vueling airlines":
        airline_name = "vueling"

    if airline_name == "wizz air malta":
        airline_name = "wizz air"

    return airline_name
