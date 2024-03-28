import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
    while True:
        """
        Get sales input data from the user
        """
        print("Please enter the sales data from the last market.")
        print("Data should be six numbers, seperated by a comma.")
        print("Example: 10, 20, 33, 46, 60, 70")

        data_str = input("Enter your data here: \n")
        
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid.")
            break
        

    return sales_data   





def validate_data(values):
    """
    checks to see if the inputted data is in the correct format,
    six comma seperated numbers, 
    Inside the try it will convert strings to ints and raise an error if 
    it cant. The loop will request data till valid
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are required, you've entered {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def update_worksheet(data, worksheet):
    """
    receives data to update relevant worksheet.
      how many sandwiches were made and how many were wasted 
     - A negative number indicates that extra sandwiches were made
        after the stock was sold out
     - A positive number indicates wastage
    """
    
    print(f"Updating {worksheet} worksheet .....\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully!\n")
    


def calculate_surplus_data(sales_row):
    """
    Compares sales with stock and calculates the surplus.

    The surplus is defined as the sales  subtracted from the stock.
      - A negative number indicates that extra sandwiches were made
        after the stock was sold out
      . A positive number indicates wastage
    """
    print("Calculating the surplus.....")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)


    return surplus_data


def get_last_5_entries_sales():
    """
    collects colums of data returns a list containing the las 5 
    enties for each sandwich
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    calculate the average for each sandwich
    """
    print("Calculating stock data \n")
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
        
    return new_stock_data
        
        


def main():
    """
    runs all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales" )
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_column = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_column)
    update_worksheet(stock_data, "stock")




print("Welcome to Love Sandwiches data processing software")
main()
