def is_valid_table(i_table):    
    table = i_table.strip()    
    return (table == "customers" or table == "orders")


def is_valid_attribute(i_attribute):
    attribute = i_attribute.strip()
    return (attribute == "customers.name" or attribute == "customers.age" 
    or attribute == "orders.customername" or attribute == "orders.product" or attribute == "orders.price")


def is_valid_constant(i_constant):    
    constant = i_constant.strip()
    result = False
  
    if(is_valid_attribute(constant)):
        result = True
    elif(constant.isnumeric()):
        result = True
    elif(isinstance(constant, str)):
        if(constant.startswith("\"") and constant.endswith("\"")):
            result = True
        elif(constant.startswith("'") and constant.endswith("'")):
            result = True

    return result


def find_valid_operator(i_simple_condition):
    simple_condition = i_simple_condition.strip()
    if(simple_condition.find("<=") != -1):
        result = "<="
    elif(simple_condition.find(">=") != -1):
        result = ">="
    elif(simple_condition.find("<>") != -1):
        result = "<>"
    elif(simple_condition.find("=") != -1):
        result = "="
    elif(simple_condition.find("<") != -1):
        result = "<"
    elif(simple_condition.find(">") != -1):
        result = ">"
    else:
        result = -1
    
    return result


def is_valid_simple_condition(i_simple_condition):
    simple_condition = i_simple_condition.strip()

    operator = find_valid_operator(simple_condition)
    if(operator == -1):        
        result = False
    else:        
        parts_array = simple_condition.split(operator)        
        result = is_valid_constant(parts_array[0]) and is_valid_constant(parts_array[1])

    return result


def is_valid_att_list(i_att_list):
    att_list = i_att_list.strip()

    if(is_valid_attribute(att_list)):
        result = True
    else:
        comma_index = att_list.find(",")
        if(comma_index == -1):
            result = False
        else:
            result = is_valid_attribute(att_list[0:comma_index]) and is_valid_att_list(att_list[comma_index+1:])
    
    return result


def is_valid_attribute_list(i_attribute_list):
    attribute_list = i_attribute_list.strip()
    index_of_astrix = attribute_list.find("*")

    if(index_of_astrix == 0):
        if(attribute_list == "*"):  # the attribute list is only *
            result = True
        else:
            result = False
    else:
        result = is_valid_att_list(attribute_list)
    
    return result


def is_valid_table_list(i_table_list):
    table_list = i_table_list.strip()
    
    if(is_valid_table(table_list)):
        result = True
    else:
        comma_index = table_list.find(",")
        if(comma_index == -1):            
            result = False
        else:
            result = is_valid_table(table_list[0:comma_index]) and is_valid_table_list(table_list[comma_index+1:])
            
    return result   


def is_valid_condition(i_condition):
    condition = i_condition.strip()
    result = False

    if(is_valid_simple_condition(condition)):
        result = True    
    else:
        checked_all_options = False
        #there has to be a space right before and right after AND & OR
        and_index = condition.find(" and ")
        or_index = condition.find(" or ")

        while(not checked_all_options and not result):
            if(and_index != -1):
                left_and_part = condition[0:and_index]
                right_and_part = condition[and_index+5:]
                if(is_valid_condition(left_and_part) and is_valid_condition(right_and_part)):
                    result=True                    
                else:
                    and_index = condition.find(" and ", and_index+5)
            elif(or_index != -1):
                left_or_part = condition[0:or_index]
                right_or_part = condition[or_index+4:]
                if(is_valid_condition(left_or_part) and is_valid_condition(right_or_part)):
                    result=True                    
                else:
                    or_index = condition.find(" or ", or_index+4)
            else:  # both indexes not found
                checked_all_options = True                

        if (not result):
            if(condition[0] == "(" and condition[-1] == ")"):                
                result = is_valid_condition(condition[1:-1])

    return result


def is_select_part_valid(i_select_part):
    result = False
    # i_select_part starts with "select" and there has to be a space right after it
    if (i_select_part[6] == " "):   
        select_part = i_select_part[6:].strip()
        distinct_index = select_part.find("distinct")
        if(distinct_index == 0):
            select_part = select_part[8:]   # attribute list starts after the distinct          
        result = is_valid_attribute_list(select_part)  

    return result


def is_from_part_valid(i_from_part):
    result = False
    # i_from_part starts with "from" and there has to be a space right after it  
    if(i_from_part[4] == " "):
        from_part = i_from_part[4:].strip()
        result = is_valid_table_list(from_part)

    return result


def is_where_part_valid(i_where_part):
    result = False        
    # i_where_part starts with "where" and there has to be a space right after it   
    if(i_where_part[5] == " "):
        where_part = i_where_part[5:].strip()
        result = is_valid_condition(where_part)    

    return result


def is_valid_query(i_query):
    result = "Valid"
    query = i_query.strip()
    query = query.lower()  # so our check is case-insensitive
    
    if(query[-1]==";"):
        query=query[0:-1]
        select_index = query.find("select")     
        from_index = query.find("from")
          
        if(not is_select_part_valid(query[select_index:from_index])):
            result = "Invalid. Parsing <attribute_list> failed"
        else:
            where_index = query.find("where")
            if(not is_from_part_valid(query[from_index:where_index])):
                result = "Invalid. Parsing <table_list> failed"
            else:
                if(not is_where_part_valid(query[where_index:])):
                    result = "Invalid Parsing <condition> failed"
    else:   #missing ; at the end of the query
       result = "Invalid Parsing <condition> failed"

    print(result)

    return result


def main():
    query  = input("Enter your query: ")    
    is_valid_query(query)


if __name__ == "__main__":
    main()
