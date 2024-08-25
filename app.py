from User.super_admin_func import after_login_super

from for_print import error, enter, success, prints, command, re_enter

from db_settings import Database, execute_query


def type_analyzer(user_type: int):
    """
    Function to analyze user type.
    """
    queries = "SELECT * FROM user WHERE type=%s"
    params = (user_type,)
    data = execute_query(query=queries, params=params, fetch="one")
    return data.get("type")


def after_login(user_type: int=None, email: str=None, super_admin: bool=False):
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

    else:
        after_login_super()


def main():
    """
    Main function to run the program
    """
    while True:
        print(command + "\n1. Login\n"
                        "2. Exit\n")
        choice: str = input(enter + "Enter: ")

        if choice == "1":
            pass
            # login()

        elif choice == "2":
            print(success + "Exiting...")
            break

        else:
            print(error + "Invalid choice. Please try again.")


after_login(super_admin=True)