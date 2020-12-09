import warnings
import math
def operate(number1,operation,number2):
	if(operation=="^"):
		return number1**number2
	elif(operation=="*"):
		return number1*number2
	elif(operation=="/"):
		return number1/number2
	elif(operation=="%"):
		return number1%number2
	elif(operation=="+"):
		return number1+number2
	elif(operation=="-"):
		return number1-number2
	else:
		raise Exception("Jasper needs to update the operate function")
def read_numbers_recursion(read_string):
	operations = ["^","*","/","%","+","-"]
	operation_order = ["^",["*","/","%"],["+","-"]]
	numbers = ['0','1','2','3','4','5','6','7','8','9','.']
	ignored_characters = [" ",","]
	as_list = []
	parenthesis_counter = 0 #
	parenthesis_content = ""
	parenthesis_start = 0 # only used for error message
	segment = ""
	last_character_was_space = False
	for char_index in range(0,len(read_string)):
		if(parenthesis_counter>0):
			if(read_string[char_index]=="("):
				parenthesis_counter+=1
			if(read_string[char_index]==")"):
				parenthesis_counter-=1
				if(parenthesis_counter==0):
					as_list.append(read_numbers_recursion(parenthesis_content))
					parenthesis_content = ""
					continue
			parenthesis_content += read_string[char_index]
		elif(read_string[char_index]=="("):
			parenthesis_start = char_index
			parenthesis_counter=1
		elif(read_string[char_index] in operations):
			if(len(segment)!=0):
				if("." in segment):
					as_list.append(float(segment))
				else:
					as_list.append(int(segment))
				segment = ""
			#check for negative number
			#if partition before this was an operation, it's a negative number, not an operation.
			if(len(as_list)==0 or as_list[len(as_list)-1] in operations):
				if(read_string[char_index]=="-"):
					segment+="-"
					continue
				elif(len(as_list)!=0):
					raise Exception( ("Two operations in a row, at index"+str(char_index-1) + "," +str(char_index)) )
			as_list.append(read_string[char_index])
		elif(read_string[char_index] in numbers):
			if(read_string[char_index-1]==" " and len(segment)!=0):
				raise Exception( ("Whitespace inside a number, at index: "+str(char_index-1) + "," +str(char_index)) )
			segment+=read_string[char_index]
		elif(not read_string[char_index] in ignored_characters):
			raise Exception( ("Unrecognized character: "+read_string[char_index]+ ", at index: " +str(char_index)))
	if(len(segment)!=0):
		if("." in segment):
			as_list.append(float(segment))
		else:
			as_list.append(int(segment))
		segment = ""
	if(parenthesis_counter!=0):
		raise Exception("Unclosed parenthesis, starting at index: "+str(parenthesis_start))
	#Why do I want to call this section folding?
	for current_operation in operation_order:
		#first and last segments cannot be operations, only numbers
		index = 1
		while index<len(as_list)-1:
			segment = as_list[index]
			#print(current_operation,index,segment)
			if((isinstance(current_operation, list) and segment in current_operation) or (segment == current_operation)):
				#print(segment,as_list)
				as_list[index] = operate(number1=as_list[index-1],operation=segment,number2=as_list[index+1])
				as_list.pop(index+1)
				as_list.pop(index-1)
				index-=2
			index+=1
	if(len(as_list)==0):
		warnings.warn("Empty input or brackets")
		return 0
	return as_list[0]


print(read_numbers_recursion('8/14.5*13^2'))

