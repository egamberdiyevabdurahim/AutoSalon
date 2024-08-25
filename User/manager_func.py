from ..for_print import error, enter, success, prints, command


def after_login_admin():
    """
    Function to handle after login as admin.
    """
    print(success + "Welcome, Admin!")
    while True:
        print(command + "\n1. Add Shopper to your Branch\n"
                        "2. Remove Shopper from your Branch\n"
                        "3. Add New CAR to your Branch\n"
                        "4. Delete CAR from your Branch\n"
                        "5. Edit Data of CAR in your Branch\n"
                        "6. View All Statistics of your Branch\n"
                        "7. View All CARS in your Branch\n"
                        "8. LogOut\n")
        choice: str = input(enter + "Enter: ")

        if choice == "1":
            ...
            # create_branch()

        elif choice == "2":
            ...
            # create_manager()

        elif choice == "3":
            ...
            # add_manager_to_branch()

        elif choice == "4":
            ...
            # delete_branch()