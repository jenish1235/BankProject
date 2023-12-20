import mysql.connector

# mysql connection, databases and tables creation
try:
        # Code for SQL connection
        sql_connection = mysql.connector.connect(
            host="localhost",
            user="jenish",
            password="jenish1235"
        )
        
        # Additional code for creating database and tables
        database_cursor = sql_connection.cursor()
        database_cursor.execute("CREATE DATABASE bank_database")
        
        db_connection = mysql.connector.connect(
            host="localhost",
            user="jenish",
            password="jenish1235",
            database="bank_database"
        )
        
        table_cursor = db_connection.cursor()
        table_cursor.execute("CREATE TABLE users (name VARCHAR(255), mobile VARCHAR(10), pin INT(4))")
        table_cursor.execute("CREATE TABLE saving_accounts (account_number INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), mobile VARCHAR(10), pin INT(4), account_balance INT(10))")
        table_cursor.execute("CREATE TABLE joint_accounts (serial_number INT NOT NULL AUTO_INCREMENT PRIMARY KEY,account_number INT(10), name VARCHAR(255), mobile VARCHAR(10), pin INT(4), account_balance INT(10))")
        table_cursor.execute("CREATE TABLE transaction_history (transaction_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, account_type VARCHAR(10), account_number INT(255), transaction_type VARCHAR(10), name VARCHAR(255), amount INT(10))")

        pass
except mysql.connector.Error as error:
        print("Failed to connect to MySQL:", error)
        db_connection = mysql.connector.connect(
            host="localhost",
            user="jenish",
            password="jenish1235",
            database="bank_database"
        )
        table_cursor = db_connection.cursor()

# banking functions

def user():
    print(""" 
          **************************************************
                            WELCOME USER
          **************************************************
          
          Do you want to :
          
          1. Sign Up
          2. Login
          
          """)
    
    user_signup_or_login = int(input("Please enter your choice: "))
    
    while True:
        # user profile creation
        if user_signup_or_login == 1:
            username = input("Please Enter Your Name: ").lower()
            mobile = input("Please Enter Your Mobile Number: ")
            user_pin = int(input("Please Set up your 4 digit pin: "))
            while True:
                if(len(str(user_pin)) == 4):
                    print("Creating New User Profile")
                    table_cursor.execute("INSERT INTO users (name,mobile,pin) values (%s,%s,%s)", [f'{username}',f'{mobile}',f'{user_pin}'])
                    db_connection.commit()
                    print("New User Profile Created Successfully")
                    break
                else:
                    print("Please set up 4 digit pin")
                    user_pin = int(input("Please Set up your 4 digit pin: "))
            banking_services()
            break
        # User Login
        elif user_signup_or_login == 2:
            username = input("Please Enter Your Name: ").lower()
            table_cursor.execute("SELECT * FROM users WHERE name = %s", [f'{username}'])
            searched_profile = table_cursor.fetchall()
            user_pin = int(input("Please Enter Your 4 digit Pin: "))
            while True:
                
                if(user_pin == searched_profile[0][2]):
                    print("Login Successfull") 
                    break
                else:
                    print("Wrong Pin, Please enter your pin again")
                    user_pin = int(input("Please Enter Your 4 digit pin: "))
            banking_services()
            break
        else:
            print("Please Enter A Valid Choice")
            user_signup_or_login = int(input("Please enter your choice: "))

def banking_services():
    # Banking Services Initiation
        print("""
              **************************************************
                        INTIATING BANKING SERVICES
              **************************************************
              
              
              **************************************************
              Please Select the service to use:
              
              1. Create New Saving Account
              2. Create New Joint Account
              3. Use Existing Bank Account
              4. Deposit Money To An Account
              5. Delete Your Profile
              6. Exit
              
              """)
        service_choice_by_user = int(input("Please Enter Your Choice: "))
        while True:
            if(service_choice_by_user == 1):
                saving_account_validity = 1
                print("""
                    ************************************************************************
                                INITIATING PROCESS FOR SAVING ACCOUNT CREATION
                    ************************************************************************
                    KINDLY COOPERATE !!!
                    """)
                
                print("**** TO GO BACK enter Account Holder Name: back **** ")
                account_holder_name = input("Please Enter Account Holder Name: ")
                if account_holder_name == "back":
                    banking_services()
                else:
                    account_holder_mobile_number = input("Please Enter Account Holder Mobile Number: ")
                    account_holder_pin = int(input("Please Set up your 4 digit account pin: "))
                    table_cursor.execute("INSERT INTO saving_accounts (name,mobile,pin,account_balance) VALUES (%s,%s,%s,0)", [f'{account_holder_name}',f'{account_holder_mobile_number}',f'{account_holder_pin}'])
                    db_connection.commit()
                    table_cursor.execute("SELECT account_number FROM saving_accounts WHERE name = %s AND mobile = %s AND pin = %s", [f'{account_holder_name}', f'{account_holder_mobile_number}', f'{account_holder_pin}'])
                    results = table_cursor.fetchone()[0]
                    print("SUCCESSFULLY CREATED YOUR SAVING ACCOUNT")
                    print(f"Your Account Number is {results}")
                    task_after_account_creation(saving_account_validity, results)          
            elif(service_choice_by_user == 2):
                saving_account_validity = 2
                print("""
                    ************************************************************************
                                INITIATING PROCESS FOR JOINT ACCOUNT CREATION
                    ************************************************************************
                    KINDLY COOPERATE !!!
                    """)
                
                print("**** TO GO BACK ENTER NUMBER OF MEMBERS 999 ****")
                number_of_members_in_joint_account = int(input("Please Enter the number of members for joint account: "))
                
                if number_of_members_in_joint_account == 999:
                    banking_services()
                else:
                    table_cursor.execute("SELECT * from joint_accounts")
                    results = table_cursor.fetchall()
                    if(len(results) == 0 ):
                        joint_account_number = 1
                    else: 
                        table_cursor.execute("SELECT max(account_number) AS joint_account_number FROM joint_accounts")
                        joint_account_number = table_cursor.fetchone()[0] + 1
                        print(joint_account_number)
                        
                    for i in range(number_of_members_in_joint_account):
                        
                        account_holder_name = input(f"Please Enter account holder name of {i+1} member: ")
                        account_holder_mobile_number = input(f"Please enter account holder mobile number {account_holder_name}: ")
                        account_holder_pin = int(input(f"Please set up 4 digit pin for {account_holder_name}: "))
                        table_cursor.execute("INSERT INTO joint_accounts (account_number,name,mobile,pin,account_balance) VALUES (%s,%s,%s,%s,%s)", [f'{joint_account_number}', f'{account_holder_name}', f'{account_holder_mobile_number}', f'{account_holder_pin}', 0])
                        db_connection.commit()
                        
                    
                    print("SUCCESSFULLY CREATED YOUR JOINT ACCOUNT")
                    task_after_account_creation(saving_account_validity,joint_account_number)      
            elif(service_choice_by_user == 3):
                print("""
                  ************************************************************************
                            LOGGING INTO YOUR BANK ACCOUNT
                  ************************************************************************
                  KINDLY COOPERATE !!!
                  
                  PLEASE SELECT YOUR ACCOUNT TYPE
                  
                  1. SAVING ACCOUNT
                  2. JOINT ACCOUNT 
                  3. GO BACK
                  """)
                user_choice_to_login_into_account = int(input("Please enter your choice: "))
                
                while True:
                    if(user_choice_to_login_into_account == 1):
                        saving_account_validity = 1
                        login_acc_number = int(input("Please Enter Your Account Number: "))
                        login_acc_pin = int(input("Please Enter your account pin: "))
                        table_cursor.execute("SELECT * FROM saving_accounts WHERE account_number = %s", [f'{login_acc_number}'])
                        fetched_Acc = table_cursor.fetchall()
                        while True:
                            if(login_acc_pin == fetched_Acc[0][3]):
                                print("LOGIN SUCCESSFULL")
                                break
                            else:
                                login_acc_pin = int(input("Please Enter your account pin: "))
                        task_after_account_creation(saving_account_validity,login_acc_number)
                        break
                    
                    elif(user_choice_to_login_into_account == 2):
                        saving_account_validity = 2
                        login_acc_number = int(input("Please Enter Your Account Number: "))
                        table_cursor.execute("SELECT * FROM joint_accounts WHERE account_number = %s", [f'{login_acc_number}'])
                        fetched_Acc = table_cursor.fetchall()
                        for i in range(len(fetched_Acc)):
                            login_acc_pin = int(input(f"Please Enter account pin for {fetched_Acc[i][2]}: "))
                            while True:
                                if(login_acc_pin == fetched_Acc[i][4]):
                                    break
                                else:
                                    login_acc_pin = int(input("Please Enter your account pin: "))
                        
                        print("LOGIN SUCCESSFULL")
                        task_after_account_creation(saving_account_validity,login_acc_number)
                        break
                    elif(user_choice_to_login_into_account == 3):
                        banking_services()
                    else:
                         user_choice_to_login_into_account = int(input("Please enter the valid choice: "))
            elif(service_choice_by_user == 4):
                saving_account_validity = int(input("""
                                                    
                                                    Please Select account type of account you want to deposit money to: 
                                                    1. Saving Account
                                                    2. Joint Account
                                                    
                                                    Enter Your Choice: 
                                                    """))
                account_number = int(input("Please Enter the account number: "))
                
                deposit(saving_account_validity,account_number)
                banking_services()
                break
            elif(service_choice_by_user == 5):
                print("""
                      **************************************************
                      Are you sure you want to delete your profile???
                      **************************************************
                      1. YES
                      2. CANCEL
                      """)
                user_profile_deletion_choice = int(input("Please Enter Your Choice: "))  
                while True:
                    if(user_profile_deletion_choice == 1):
                        username = input("Please Enter your username: ")
                        mobile = input("Please Enter your registered mobile number: ")
                        pin = int(input("Please Enter your pin"))
                        table_cursor.execute("DELETE FROM users WHERE name = %s AND mobile = %s AND pin = %s", [f'{username}', f'{mobile}',f'{pin}'])
                        db_connection.commit()
                        print("PROFILE SUCCESSFULLY DELETED")
                        exit()
                    elif(user_profile_deletion_choice == 2):
                        banking_services()
                        break
                break
            elif(service_choice_by_user == 6):
                exit()
            else:
                service_choice_by_user = int(input("Please Enter Valid Choice: "))

def task_after_account_creation(saving_account_validity, account_number):
    while True:
                        print("""
                              **************************************************
                                                PLEASE SELECT A TASK
                              **************************************************
                              
                              1. GET ACCOUNT INFO
                              2. GET ACCOUNT BALANCE
                              3. DEPOSIT MONEY
                              4. WITHDRAW MONEY
                              5. GET TRANSACTION HISTORY
                              6. CLOSE ACCOUNT
                              7. GO BACK
                              
                              """)
                        user_choice_to_perform_task  = int(input("Please Enter Your Choice: "))
                        
                        while True:
                            if(user_choice_to_perform_task == 1):
                                get_account_info(saving_account_validity, account_number)
                                break
                            elif(user_choice_to_perform_task == 2):
                                get_account_balance(saving_account_validity, account_number)
                                break
                            elif(user_choice_to_perform_task == 3):
                                deposit(saving_account_validity, account_number)
                                break
                            elif(user_choice_to_perform_task == 4):
                                withdraw(saving_account_validity, account_number)
                                break
                            elif(user_choice_to_perform_task == 5):
                                get_transaction_history(saving_account_validity, account_number)
                                break
                            elif(user_choice_to_perform_task == 6):
                                close_account(saving_account_validity, account_number)
                                banking_services()
                                break
                            elif(user_choice_to_perform_task == 7):
                                banking_services()
                                break
                            else:
                                user_choice_to_perform_task  = int(input("Please Enter A Valid Choice: "))

def get_account_info(saving_account_validity,account_number):
    if(saving_account_validity == 1):
        table_cursor.execute("SELECT  * FROM saving_accounts WHERE account_number = %s", [f'{account_number}'])
        results = table_cursor.fetchall()[0]
        print(f"""
                  **************************************************
                  Account Number: {results[0]}
                  Account Holder Name: {results[1]}
                  Account Holder Mobile: {results[2]}
                  
                  **************************************************
                  """)
    elif(saving_account_validity == 2):
        table_cursor.execute("SELECT  * FROM joint_accounts WHERE account_number = %s", [f'{account_number}'])
        results = table_cursor.fetchall()
        for i in range(len(results)):
                print(f"""
                  **************************************************
                  Account Number: {results[i][1]}
                  Member: {i+1}
                  Account Holder Name: {results[i][2]}
                  Account Holder Mobile: {results[i][3]}
                  
                  **************************************************
                  """)
                
def get_account_balance(saving_account_validity,account_number):
    if (saving_account_validity == 1):
        table_cursor.execute("SELECT account_balance FROM saving_accounts WHERE account_number = %s", [f'{account_number}'])
        results = table_cursor.fetchone()
        print(f"""
              **************************************************
              YOUR ACCOUNT BALANCE: {results[0]}
              **************************************************
              """)
    elif(saving_account_validity == 2):
        table_cursor.execute("SELECT account_balance FROM joint_accounts WHERE account_number = %s", [f'{account_number}'])
        current_account_balance = table_cursor.fetchall()[0][0]
        print(f"""
              **************************************************
              YOUR ACCOUNT BALANCE: {current_account_balance}
              **************************************************
              """)

def deposit(saving_account_validity, account_number):
    transaction_type = 'CREDITED'
    if(saving_account_validity == 1):
        account_type = 'saving'
        table_cursor.execute("SELECT account_balance FROM saving_accounts WHERE account_number = %s ", [f'{account_number}'])
        current_account_balance = table_cursor.fetchall()[0][0]
        print("************************************************** MONEY DEPOSIT **************************************************")
        name = input("Please Enter Your name to proceed with the transaction: ")
        amount = int(input("Please Enter the amount of Money to deposit: "))
        new_account_balance = current_account_balance + amount
        table_cursor.execute("UPDATE saving_accounts SET account_balance  = %s WHERE account_number = %s", [f'{new_account_balance}', f'{account_number}'])
        table_cursor.execute("INSERT INTO transaction_history (account_type, account_number, transaction_type, name, amount) VALUES (%s,%s,%s,%s,%s)", [f'{account_type}',f'{account_number}', f'{transaction_type}', f'{name}', f'{amount}'])
        db_connection.commit()
        print(f"**************************************************Updated Account Balance: {new_account_balance} **************************************************") 
    elif(saving_account_validity == 2):
        account_type = 'joint'
        table_cursor.execute("SELECT account_balance FROM joint_accounts WHERE account_number = %s ", [f'{account_number}'])
        current_account_balance = table_cursor.fetchall()
        current_account_balance = current_account_balance[0][0]
        print("************************************************** MONEY DEPOSIT **************************************************")
        name = input("Please Enter Your name to proceed with the transaction: ")
        amount = int(input("Please Enter the amount of Money to deposit: "))
        new_account_balance = current_account_balance + amount
        table_cursor.execute("UPDATE joint_accounts SET account_balance  = %s WHERE account_number = %s", [f'{new_account_balance}', f'{account_number}'])
        table_cursor.execute("INSERT INTO transaction_history (account_type, account_number, transaction_type, name, amount) VALUES (%s,%s,%s,%s,%s)", [f'{account_type}',f'{account_number}', f'{transaction_type}', f'{name}', f'{amount}'])
        db_connection.commit()
        print(f"**************************************************Updated Account Balance: {new_account_balance} **************************************************") 

def withdraw(saving_account_validity, account_number):
    transaction_type = 'DEBITED'
    if(saving_account_validity == 1):
        account_type = 'saving'
        table_cursor.execute("SELECT account_balance FROM saving_accounts WHERE account_number = %s ", [f'{account_number}'])
        current_account_balance = table_cursor.fetchall()[0][0]
        print("************************************************** MONEY WITHDRAW **************************************************")
        name = input("Please Enter Your name to proceed with the transaction: ")
        amount = int(input("Please Enter the amount of Money to withdraw: "))
        while True:
            if(amount < current_account_balance):
                new_account_balance = current_account_balance - amount
                break
            else:
                print("*** PLEASE ENTER AMOUNT LESS THAN CURRENT BALANCE ***")
                print(f"CURRENT ACCOUNT BALANCE: {current_account_balance}")
                amount = int(input("Please Enter the amount of Money to withdraw: "))
                
        table_cursor.execute("UPDATE saving_accounts SET account_balance  = %s WHERE account_number = %s", [f'{new_account_balance}', f'{account_number}'])
        table_cursor.execute("INSERT INTO transaction_history (account_type, account_number, transaction_type, name, amount) VALUES (%s,%s,%s,%s,%s)", [f'{account_type}',f'{account_number}', f'{transaction_type}', f'{name}', f'{amount}'])
        db_connection.commit()
        print(f"**************************************************Updated Account Balance: {new_account_balance} **************************************************")
    elif(saving_account_validity == 2):
        account_type = 'joint'
        table_cursor.execute("SELECT account_balance FROM joint_accounts WHERE account_number = %s ", [f'{account_number}'])
        current_account_balance = table_cursor.fetchall()[0][0]
        print("************************************************** MONEY WITHDRAW **************************************************")
        name = input("Please Enter Your name to proceed with the transaction: ")
        amount = int(input("Please Enter the amount of Money to withdraw: "))
        while True:
            if(amount < current_account_balance):
                new_account_balance = current_account_balance - amount
                break
            else:
                print("*** PLEASE ENTER AMOUNT LESS THAN CURRENT BALANCE ***")
                print(f"CURRENT ACCOUNT BALANCE: {current_account_balance}")
                amount = int(input("Please Enter the amount of Money to withdraw: "))
                
        table_cursor.execute("UPDATE joint_accounts SET account_balance  = %s WHERE account_number = %s", [f'{new_account_balance}', f'{account_number}'])
        table_cursor.execute("INSERT INTO transaction_history (account_type, account_number, transaction_type, name, amount) VALUES (%s,%s,%s,%s,%s)", [f'{account_type}',f'{account_number}', f'{transaction_type}', f'{name}', f'{amount}'])
        db_connection.commit()
        print(f"**************************************************Updated Account Balance: {new_account_balance} **************************************************")

def get_transaction_history(saving_account_validity,account_number):
    if(saving_account_validity == 1):
        table_cursor.execute("SELECT * FROM transaction_history WHERE account_type = 'saving' AND account_number =  %s", [f'{account_number}'])
        results = table_cursor.fetchall()
        print("""
              *****************************************************************************************
                                                SHOWING TRANSACTION HISTORY 
              *****************************************************************************************
              
              """)
        for i in range(len(results)):
            print(f'Transaction ID: {results[i][0]} ')
            print(f'Account Type: {results[i][1]}')
            print(f'Account Number: {results[i][2]}')
            print(f'Transaction Type: {results[i][3]}')
            print(f'Name of Transactor: {results[i][4]}')
            print(f'Amount: {results[i][5]}')
            print('**************************************')
        print("""
              ******************************************************************************************************************************************
              """)
    elif(saving_account_validity == 2):
        table_cursor.execute("SELECT * FROM transaction_history WHERE account_type = 'joint' AND account_number =  %s", [f'{account_number}'])
        results = table_cursor.fetchall()
        print("""
              ******************************************************************************************************************************************
                                                                                    SHOWING TRANSACTION HISTORY 
              ******************************************************************************************************************************************
              
              """)
        for i in range(len(results)):
            print(f'Transaction ID: {results[i][0]} ')
            print(f'Account Type: {results[i][1]}')
            print(f'Account Number: {results[i][2]}')
            print(f'Transaction Type: {results[i][3]}')
            print(f'Name of Transactor: {results[i][4]}')
            print(f'Amount: {results[i][1]}')
            print('**************************************')
        
        print("""
              ******************************************************************************************************************************************
              """)

def close_account(saving_account_validity, account_number):
    if(saving_account_validity == 1):
        table_cursor.execute("DELETE FROM saving_accounts WHERE account_number = %s", [f'{account_number}'])
        db_connection.commit()
        print("""
              **************************************************
                        ACCOUNT DELETED SUCCESSFULLY
              **************************************************
              """)
    elif(saving_account_validity == 2):
        table_cursor.execute("DELETE FROM joint_accounts WHERE account_number = %s", [f'{account_number}'])
        db_connection.commit()
        print("""
              **************************************************
                        ACCOUNT DELETED SUCCESSFULLY
              **************************************************
              """)

def employee():
    employee_pwd = int(input("Please Enter Employee Pin: "))
    if(employee_pwd == 9898):
        print("Please Select Operation: 1. View All Transaction History 2. View All Accounts")
        choice = int(input("Enter Your choice: "))
        
        if(choice == 1):
            table_cursor.execute("SELECT * from transaction_history")
            results = table_cursor.fetchall()
            for i in range(len(results)):
                print(results[i])
            restart()
        elif(choice == 2):
            print("Please Select Account Type: 1. Saving 2. Joint")
            choice_acc = int(input("Please Enter Your Choice: "))
            if(choice_acc == 1):
                table_cursor.execute("SELECT * FROM saving_accounts")
                results = table_cursor.fetchall()
                for i in range(len(results)):
                    print(results[i])
                restart()
            elif(choice_acc == 2):
                table_cursor.execute("SELECT * FROM joint_accounts")
                results = table_cursor.fetchall()
                for i in range(len(results)):
                    print(results[i])
                restart()
        else:
            print("Wrong employee pin")
            restart()
        
   
                
def restart():
    print("""
          
          **************************************************
          Please Select What describes you best:
          
          1. USER
          2. EMPLOYEE          
          """)
    while True:
        user_or_employee_selection = int(input("Please enter your choice: "))
        if(user_or_employee_selection == 1):
            user()
            break
        elif(user_or_employee_selection == 2):
            employee()
            break
        else:
            print("Please enter a valid choice")
            user_or_employee_selection = int(input("Please enter your choice: "))
# Program Entry Point
if __name__ == "__main__":
    
# welcome message
    print("""
          
          **************************************************
                            WELCOME TO BANK
          **************************************************
          
          """)
    restart()
