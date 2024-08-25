from for_print import error, enter, re_enter, success, prints, command
from jsonfilemanager import JSONFIleManager
from db_settings import Database, execute_query
from User.super_admin_func import SuperAdmin


#super_admin user = super
#super_admin password= super


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
            pass

        elif user_type == "Shopper":
            pass

        elif user_type == "User":
            pass


def login():
    username = input(command + "Username: ")
    password = input(command + "Password: ")
    if username == 'super' and password == 'super':
        SuperAdmin.after_login_super()


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
