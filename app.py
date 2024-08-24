from for_print import error, enter, success, prints, command


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