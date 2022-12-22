#!/usr/bin/env python3 

dict_1 = {"b":2, "c":3, "aa":4}
if dict_1.get("a") is not None:
	print("Exists")
else:
	print("Does not exist")

if "a" in dict_1:
	print ("captured by in")
#Output = "Exists"
