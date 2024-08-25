from for_print import error, enter, success, prints, command
from User.superadminmanager import create_branch
from db_settings import Database, execute_query


def after_login_super():
    """
    Function to handle after login as super admin.
    """
    while True:
        print(command + "\n1. Create New Branch\n"
                        "2. Create New Manager And Add to Branch\n"
                        "3. Add Manager To Branch\n"
                        "4. View All Statistics of Company\n"
                        "5. View All Statistics of One Branch\n"
                        "6. LogOut\n")
        choice: str = input(enter + "Enter: ")

        if choice == "1":
            branch_name = input(enter + "Enter Branch Name: ")
            if create_branch(branch_name):
                print('Successfully branch created!')
            else:
                print(error + 'Unsuccessful try!')
            # create_branch()

        elif choice == "2":
            pass
            # create_manager_and_add_to_branch()

        elif choice == "3":
            pass
            # add_manager_to_branch()

        elif choice == "4":
            pass
            # view_all_statistics_of_company()

        elif choice == "5":
            pass
            # view_all_statistics_of_one_branch()

        elif choice == "6":
            print(success + "Logged out successfully.")
            return None

        else:
            print(error + "Invalid choice. Please try again.")
