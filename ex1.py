def is_valid_table(i_table):
    table = i_table.strip()
    return (table == "Customers" or table == "Orders")


def is_valid_attribute(i_attribute, i_tables):
    attribute = i_attribute.strip()
    result = False
    for table in i_tables:
        if(attribute.startswith(table)):
            result = (attribute == "Customers.Name" or attribute == "Customers.Age"
                      or attribute == "Orders.CustomerName" or attribute == "Orders.Product" or attribute == "Orders.Price")

    return result


def get_attribute_type(i_attribute):
    att_type = None

    if(i_attribute == "Customers.Name" or i_attribute == "Orders.CustomerName" or i_attribute == "Orders.Product"):
        att_type = "string"
    elif(i_attribute == "Customers.Age" or i_attribute == "Orders.Price"):
        att_type = "int"

    return att_type

# returns a tuple: 1st element-bool and 2nd element- type of constant.
def is_valid_constant(i_constant, i_tables):
    constant = i_constant.strip()
    result = False
    constant_type = None

    if(is_valid_attribute(constant, i_tables)):
        result = True
        constant_type = get_attribute_type(constant)
    elif(constant.isnumeric()):
        result = True
        constant_type = "int"
    elif(isinstance(constant, str)):
        if((constant.startswith("\"") and constant.endswith("\""))
           or (constant.startswith("'") and constant.endswith("'"))):
            result = True
            constant_type = "string"

    return (result, constant_type)


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


def is_valid_simple_condition(i_simple_condition, i_tables):
    simple_condition = i_simple_condition.strip()
    result = False

    operator = find_valid_operator(simple_condition)
    if(operator != -1):
        parts_array = simple_condition.split(operator)
        (const1_result, const1_type) = is_valid_constant(
            parts_array[0], i_tables)
        (const2_result, const2_type) = is_valid_constant(
            parts_array[1], i_tables)
        if(const1_result and const2_result):
            if(const1_type == const2_type):
                result = True

    return result


def is_valid_att_list(i_att_list, i_tables):
    att_list = i_att_list.strip()

    if(is_valid_attribute(att_list, i_tables)):
        result = True
    else:
        comma_index = att_list.find(",")
        if(comma_index == -1):
            result = False
        else:
            result = is_valid_attribute(att_list[0:comma_index], i_tables) and is_valid_att_list(
                att_list[comma_index+1:], i_tables)

    return result


def is_valid_attribute_list(i_attribute_list, i_tables):
    attribute_list = i_attribute_list.strip()
    index_of_astrix = attribute_list.find("*")

    if(index_of_astrix == 0):
        if(attribute_list == "*"):  # the attribute list is only *
            result = True
        else:
            result = False
    else:
        result = is_valid_att_list(attribute_list, i_tables)

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
            result = is_valid_table(table_list[0:comma_index]) and is_valid_table_list(
                table_list[comma_index+1:])

    return result

# function used in is_valid_condition
def check_both_sides_of_operator(i_condition, i_operator, i_index, i_result, i_checked_all_options, i_tables):
    if(i_operator == "AND"):
        offset = 3
    elif(i_operator == "OR"):
        offset = 2

    if(i_condition[i_index-1] == ")" or i_condition[i_index-1] == " "):
        if(i_condition[i_index+offset] == "(" or i_condition[i_index+offset] == " "):
            left_operator_part = i_condition[0:i_index]
            right_operator_part = i_condition[i_index+offset:]
            if(is_valid_condition(left_operator_part, i_tables) and is_valid_condition(right_operator_part, i_tables)):
                i_result = True
            else:
                i_index = i_condition.find(
                    i_operator, i_index+offset)
        else:
            i_checked_all_options = True
    else:
        i_checked_all_options = True
    return(i_index, i_result, i_checked_all_options)


def is_valid_condition(i_condition, i_tables):
    condition = i_condition.strip()
    result = False

    if(is_valid_simple_condition(condition, i_tables)):
        result = True
    else:
        checked_all_options = False
        and_index = condition.find("AND")
        or_index = condition.find("OR")

        while(not checked_all_options and not result):
            if(and_index != -1):
                #check_both_sides_of_operator function includes the recursive call to is_valid_simple_condition
                (and_index, result, checked_all_options) = check_both_sides_of_operator(
                    condition, "AND", and_index, result, checked_all_options, i_tables)
            elif(or_index != -1):
                (or_index, result, checked_all_options) = check_both_sides_of_operator(
                    condition, "OR", or_index, result, checked_all_options, i_tables)
            else:  # both indexes not found
                checked_all_options = True
                if (not result):
                    if(condition[0] == "(" and condition[-1] == ")"):
                        result = is_valid_condition(condition[1:-1], i_tables)

    return result


def is_select_part_valid(i_select_part, i_tables):
    result = False
    # i_select_part starts with "select" and there has to be a space right after it
    if (i_select_part[6] == " "):
        select_part = i_select_part[6:].strip()
        distinct_index = select_part.find("DISTINCT")
        if(distinct_index == 0):
            # attribute list starts after the distinct
            select_part = select_part[8:]
        result = is_valid_attribute_list(select_part, i_tables)

    return result


def decipher_table_list(i_from_part):
    table_list = i_from_part.split(",")
    # for table in result:
    #     table = table.strip()
    table_list = list(map(str.strip, table_list))

    return table_list

# returns a tuple: 1st element-bool and 2nd element-a list of tables.
def is_from_part_valid(i_from_part):
    result = False
    table_list = None

    # i_from_part starts with "from" and there has to be a space right after it
    if(i_from_part[4] == " "):
        from_part = i_from_part[4:].strip()
        result = is_valid_table_list(from_part)
        if(result):
            table_list = decipher_table_list(from_part)

    return (result, table_list)


def is_where_part_valid(i_where_part, i_tables):
    result = False
    # i_where_part starts with "where" and there has to be a space right after it
    if(i_where_part[5] == " "):
        where_part = i_where_part[5:].strip()
        result = is_valid_condition(where_part, i_tables)

    return result


def is_valid_query(i_query):
    result = "Valid"
    query = i_query.strip()

    if(query[-1] == ";"):
        query = query[0:-1]

        select_index = query.find("SELECT")
        from_index = query.find("FROM")
        where_index = query.find("WHERE")

        (from_result, table_list) = is_from_part_valid(
            query[from_index:where_index])

        if(not from_result):
            result = "Invalid. Parsing <table_list> failed"
        else:
            if(not is_select_part_valid(query[select_index:from_index], table_list)):
                result = "Invalid. Parsing <attribute_list> failed"
            else:
                if(not is_where_part_valid(query[where_index:], table_list)):
                    result = "Invalid Parsing <condition> failed"
    else:  # missing ; at the end of the query
        result = "Invalid Parsing <condition> failed"

    print(result)

    return result


def main():
    query = input("Enter your query: ")
    is_valid_query(query)


if __name__ == "__main__":
    main()
