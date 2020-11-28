import ex1;

tests = [
    # {
    #     "query": "SELECT          Customers.Name FROM  Customers WHERE ((Customers.Name='Mike') AND Orders.Price>1000);",
    #     "expected": "Invalid Parsing <condition> failed",
    # },
    # {
    #     "query": "SELECT * Customers.Name FROM  Customers WHERE ((Customers.Name='Mike') AND Orders.Price>1000);",
    #     "expected": "Invalid. Parsing <attribute_list> failed",
    # },
    {
        "query": "SELECT * FROM Customers, Orders WHERE ((Customers.Name='Mike') AND Orders.Price>1000) OR 'x'=1;",
        "expected": "Valid",
     },
    # {
    #     "query": "SELECT *,Customers.Name FROM Customers, Orders WHERE ((Customers.Name='Mike') AND Orders.Price>1000) OR 'x'=1;",
    #     "expected": "Invalid. Parsing <attribute_list> failed",
    # },
    # {
    #     "query": "SELECT  DISTINCT  Customers.Name FROM Customers Orders WHERE ((Customers.Name='Mike') AND Orders.Price>1000) OR 'x'=1;",
    #     "expected": "Invalid. Parsing <table_list> failed",
    # },
    #  {
    #     "query": "SELECT Customers.Name FROM Customers WHERE Customers.Age=25;",
    #     "expected": "Valid",
    # },
    # {
    #     "query": "   SELECT Customers.Name FROM Customers WHERE    Customers.Name='Mike'      ;",
    #     "expected": "Valid",
    # },
    # {
    #     "query": "SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE Customers.Name=Orders.CustomerName;",
    #     "expected": "Valid",
    # },
    # {
    #     "query": "SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE Customers.Name=Orders.CustomerName AND Orders.Price>1000;",
    #     "expected": "Valid",
    # },
    #  {
    #     "query": "SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE (Customers.Name=Orders.CustomerName) AND Orders.Price>1000;",
    #     "expected": "Valid",
    # },
    # {
    #     "query": "SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE (Customers.Name=Orders.CustomerName) OR (Orders.Price>59);",
    #     "expected": "Valid",
    # },
    # {
    #     "query": "SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE (Customers.Name=Orders.CustomerName) OR (Orders.Price>1000;",
    #     "expected": "Invalid Parsing <condition> failed",
    # },
    # {
    #     "query": "SELECT Customers.Color,Orders.Price FROM Customers,Orders WHERE (Customers.Name=Orders.CustomerName) OR (Orders.Price>1000;",
    #     "expected": "Invalid. Parsing <attribute_list> failed",
    # }
]

def main():
    for test in tests:
        actual = ex1.is_valid_query(test["query"])
        if (actual != test["expected"]):
            print("***** Failed test!: " + test["query"] + " ----- actual result: " + actual)


if __name__ == "__main__":
    main()
