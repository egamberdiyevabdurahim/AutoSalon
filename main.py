from for_print import error, enter, re_enter, success, prints, command
from jsonfilemanager import JSONFIleManager
from db_settings import Database, execute_query
from User.super_admin_func import SuperAdmin


# super_admin user = super
# super_admin password = super

def type_analyzer(user_type: int):
    """
    Function to analyze user type.
    """
    queries = "SELECT * FROM user WHERE type=%s"
    params = (user_type,)
    data = execute_query(queries, params)
    return data.get("type")


def after_login(user_type: int, email: str, super_admin: bool = False):
    """
    Function to handle after login status.
    """
    if not super_admin:
        user_type_name = type_analyzer(user_type)

        if user_type_name == "Manager":
            print(success + f"Welcome, {user_type_name}!")
            # Add Manager-specific actions here

        elif user_type_name == "Shopper":
            print(success + f"Welcome, {user_type_name}!")
            # Add Shopper-specific actions here

        elif user_type_name == "User":
            print(success + f"Welcome, {user_type_name}!")
            # Add User-specific actions here

        else:
            print(error + "Unknown user type.")

    else:
        # Handle super admin actions
        SuperAdmin.after_login_super()


def login():
    """
    Function to handle user login.
    """
    username = input(command + "Username: ")
    password = input(command + "Password: ")

    if username == 'super' and password == 'super':
        after_login(user_type=None, email=username, super_admin=True)
    else:
        # Fetch user data from the database
        user_query = "SELECT * FROM user WHERE username=%s AND password=%s"
        user_params = (username, password)
        user_data = execute_query(user_query, user_params)

        if user_data:
            user_type = user_data.get("type")
            email = user_data.get("email")
            after_login(user_type=user_type, email=email)
        else:
            print(error + "Invalid username or password.")


def main():
    """
    Main function to run the program
    """
    while True:
        print(command + "\n1. Login\n"
                        "2. Exit\n")
        choice: str = input(enter + "Enter: ")

        if choice == "1":
            login()

        elif choice == "2":
            print(success + "Exiting...")
            break

        else:
            print(error + "Invalid choice. Please try again.")


if __name__ == '__main__':
    main()

