
def is_valid_simple_condition(i_simple_condition):
    pass


def is_valid_condition(i_condition):
    condition = i_condition.strip()
    if(is_valid_simple_condition(condition)):
        result = True
    else:
        pass
    return result


def is_where_part_valid(i_where_part):
    if(i_where_part[5] == " "):
        where_part = i_where_part.strip()
        result = is_valid_condition(where_part[5:])
        print("space is  ok")

    else:
        print("space is not ok")
        result = False

    return result


def is_valid_table(i_table):
    print(i_table)
    table = i_table.strip()
    if(table == "Customers" or table == "Orders"):
        print("table ok")
    else:
        print("table not ok")
    return table == "Customers" or table == "Orders"


def is_valid_table_list(i_table_list):
    table_list = i_table_list.strip()
    if(is_valid_table(table_list)):
        result = True
    else:
        comma_index = table_list.find(",")
        if(comma_index == -1):
            print("missing comma")
            result = False
        else:
            result = is_valid_table_list(table_list[comma_index+1:])
            print(" comma ok")
    return result


def is_from_part_valid(i_from_part):
    if(i_from_part[4] == " "):
        from_part = i_from_part.strip()
        result = is_valid_table_list(from_part[4:])
        print("space is  ok")

    else:
        print("space is not ok")
        result = False

    return result


def is_valid_attribute(i_attribute):
    attribute = i_attribute.strip()
    return attribute == "Customers.Name" or attribute == "Customers.Age" or attribute == "Orders.CustomerName" or attribute == "Orders.Product" or attribute == "Orders.Price"
# Customers(Name: STRING, Age: INTEGER)
# Orders(CustomerName: STRING, Product: STRING, Price: INTEGRER)


def is_valid_att_list(i_att_list):
    att_list = i_att_list.strip()
    if(is_valid_attribute(att_list)):
        result = True
    else:
        comma_index = att_list.find(",")
        if(comma_index == -1):
            result = False
        else:
            result = is_valid_att_list(att_list[comma_index+1:])
    return result


def is_valid_attribute_list(i_attribute_list):
    attribute_list = i_attribute_list.strip()
    index_of_astrix = attribute_list.find("*")
    if(index_of_astrix == 0):
        if(attribute_list.count == 1):
            result = True
        else:
            result = False
    else:
        result = is_valid_att_list(attribute_list)
    return result


def is_select_part_valid(i_select_part):
    select_part = i_select_part.strip()
    index_of_distinct = select_part.find("DISTINCT")
    if(index_of_distinct == 0):
        select_part = select_part[8:]
    result = is_valid_attribute_list(select_part)
    return result


def is_valid_query(i_query):
    result = "valid"
    query = i_query.strip()
    index_of_select = query.find("SELECT")
    if(index_of_select != 0 or query[6] != " "):
        result = "invalid Parsing <attribute_list> failed"
    else:
        index_of_from = query.find("FROM")
        if(not is_select_part_valid(query[6:index_of_from])):
            result = "invalid Parsing <attribute_list> failed"
        else:
            index_of_where = query.find("WHERE")
            if(not is_from_part_valid(query[index_of_from:index_of_where])):
                result = "invalid Parsing <table_list> failed"
            else:
                if(not is_where_part_valid(query[index_of_where:])):
                    result = "invalid Parsing <condition> failed"
    print(result)


# customers = {}
# customers["Name"]="STRING"
# customers["Age"]="INTEGER"
# orders = {}
# orders["CustomerName"]="STRING"
# orders["Product"] = "STRING"
# orders["Price"] = "INTEGER"
query = "SELECT  Orders.Price FROM Customers, Orders  WHERE Customer.Age=25;"
is_valid_query(query)
