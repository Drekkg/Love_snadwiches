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

        data_str = input("Enter your data here: ")
        
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
    it cant.
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

data = get_sales_data()
print(data)
