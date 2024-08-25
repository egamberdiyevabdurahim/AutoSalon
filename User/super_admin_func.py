from for_print import error, enter, success, prints, command, re_enter

from db_settings import Database, execute_query

from .addition import email_details, phone_details


def create_branch():
    """
    Function to create a new branch.
    """
    name: str = input("Enter Name: ")

    mess: bool = True
    while name == "" or name.isspace():
        print(error + "Invalid Name enter stop for Exit")
        name = input(re_enter+"Re-Enter: ")

        if name.lower() == "stop":
            mess: bool = False

    if mess:
        queries = "INSERT INTO branch (name) VALUES (%s)"
        params = (name,)
        execute_query(query=queries, params=params)
        print(success + "New branch created successfully.")
    return after_login_super()


def delete_branch():
    """
    Function to delete a branch.
    """
    while True:
        print(prints + "All Branches:")
        branches = execute_query(query="SELECT id, name FROM branch", fetch="all")
        if not branches:
            print(error + "No branches found.")
            return after_login_super()

        for branch in branches:
            print(f"{branch[0]}. {branch[1]}")

        choice: str = input(enter + "Enter Branch ID to delete or stop for Exit: ")

        if choice == "stop":
            return after_login_super()

        for branch in branches:
            if int(choice) == branch[0]:
                queries = "DELETE FROM branch WHERE id=%s"
                params = (choice,)
                execute_query(query=queries, params=params)
                print(success + "Branch deleted successfully.")
                return after_login_super()

        print(error + "Invalid Branch ID")


def edit_branch_name():
    """
    Function to edit branch name.
    """
    while True:
        print(prints + "All Branches:")
        branches = execute_query(query="SELECT * FROM branch", fetch="all")
        if not branches:
            print(error + "No branches found.")
            return after_login_super()

        for branch in branches:
            print(f"{branch[0]}. {branch[1]}")

        choice: str = input(enter + "Enter Branch ID to edit or stop for Exit: ")

        if choice == "stop":
            return after_login_super()

        for branch in branches:
            print(branch)
            if int(choice) == branch[0]:
                new_name: str = input("Enter New Name: ")

                mess: bool = True
                while len(new_name) < 2:
                    print(error + "Invalid Name, must be greater than 2 enter stop for Exit")
                    new_name = input(re_enter + "Re-Enter: ")

                    if new_name.lower() == "stop":
                        mess: bool = False

                if mess:
                    queries = "UPDATE branch SET name=%s WHERE id=%s"
                    params = (new_name, choice)
                    execute_query(query=queries, params=params)
                    print(success + "Branch name updated successfully.")
                return after_login_super()

        print(error + "Invalid Branch ID")


def view_all_branches():
    """
    Function to view all branches.
    """
    branches = execute_query(query="SELECT * FROM branch", fetch="all")
    if not branches:
        print(error + "No branches found.")
        return after_login_super()

    for branch in branches:
        print(f"ID: {branch[0]}\n"
              f"Name: {branch[1]}\n"
              f"Manager ID: {branch[2]}\n"
              f"Created At: {branch[3]}")
        print("--------------------------------------------")
    return after_login_super()


def create_manager():
    """
    Function to create a new manager.
    """
    first_name: str = input("Enter First Name: ")
    while not first_name.isalpha():
        print(error + "Invalid First Name enter stop for Exit")
        first_name = input(re_enter + "Re-Enter: ")

        if first_name.lower() == "stop":
            return after_login_super()

    last_name: str = input("Enter Last Name: ")
    while not last_name.isalpha():
        print(error + "Invalid Last Name enter stop for Exit")
        last_name = input(re_enter + "Re-Enter: ")

        if last_name.lower() == "stop":
            return after_login_super()

    email: str = input("Enter Email: ")
    while not email.endswith(email_details):
        print(error + "Invalid Email enter stop for Exit")
        email = input(re_enter + "Re-Enter: ")

        if email.lower() == "stop":
            return after_login_super()

    phone_number: str = input("Enter Phone Number: ")
    while not phone_number.startswith(phone_details):
        print(error + "Invalid Phone Number enter stop for Exit")
        phone_number = input(re_enter + "Re-Enter: ")

        if phone_number.lower() == "stop":
            return after_login_super()

    queries_province = "SELECT * FROM province"
    data = execute_query(query=queries_province, fetch="all")
    datas = []
    for column in data:
        print(f"{column[0]}: {column[1]}")
        datas.append(column[0])

    province_id: str = input("Enter Province ID: ")
    while province_id not in str(datas[0]):
        print(error + "Invalid Province ID enter stop for Exit")
        province_id = input(re_enter + "Re-Enter: ")

        if province_id.lower() == "stop":
            return after_login_super()

    password : str = input("Enter New Password: ")
    while len(password) < 8:
        print(error + "Password must be at least 8 characters long.\n"
                            "stop for Exit")
        password = input(re_enter + "Re-Enter password: ")
        if password.lower() == "stop":
            return after_login_super()

    types = execute_query("SELECT * FROM user_type WHERE name=%s", ("Manager",), "one")

    queries = "INSERT INTO users (first_name, last_name, email, phone_number, password, province_id, type_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    params = (first_name, last_name, email, phone_number, password, int(province_id), int(types.get("id")))
    execute_query(query=queries, params=params)
    print(success + "New manager created successfully.")
    choice_for_branching: str = input("Do you want to add this manager to branch(y/n): ")
    if choice_for_branching.lower() == "y":
        return add_manager_to_branch(email)
    return after_login_super()


def edit_manager_info():
    """
    Function to edit manager information.
    """
    while True:
        print(prints + "All Managers:")
        types = execute_query(query="SELECT * FROM user_type", fetch="all")
        type_for_manager = None
        for type_ in types:
            if str(type_["name"]).lower() == "manager":
                type_for_manager = type_["id"]
                break
        managers = execute_query(query="SELECT * FROM users WHERE type_id=%s", params=(type_for_manager,), fetch="all")
        for manager in managers:
            print(f"{manager['id']}: {manager['first_name']} {manager['last_name']}")

        choice: str = input(enter + "Enter Manager ID to edit or stop for Exit: ")

        if choice == "stop":
            return after_login_super()

        for manager in managers:
            if int(choice) == manager[0]:
                queries = "SELECT * FROM users WHERE id=%s"
                params = (choice,)
                data_of_manager = execute_query(query=queries, params=params, fetch="one")

                if data_of_manager is None:
                    print(error + "Manager not found.")
                    return after_login_super()

                provinces = execute_query(query="SELECT * FROM province", fetch="all")

                first_name: str = input(f"Enter New First Name or tap enter for skip (current: {data_of_manager['first_name']}): ")
                if first_name == "" or first_name.isspace():
                    first_name = data_of_manager['first_name']

                last_name: str = input(f"Enter New Last Name or tap enter for skip (current: {data_of_manager['last_name']}): ")
                if last_name == "" or last_name.isspace():
                    last_name = data_of_manager['last_name']

                email: str = input(f"Enter New Email or tap enter for skip (current: {data_of_manager['email']}): ")
                if email == "" or email.isspace():
                    email = data_of_manager['email']

                phone_number: str = input(f"Enter New Phone Number or tap enter for skip (current: {data_of_manager['phone_number']}): ")
                if phone_number == "" or phone_number.isspace():
                    phone_number = data_of_manager['phone_number']
                for province in provinces:
                    if province["id"] == data_of_manager['province_id']:
                        print(f"Current: {province['id']}. {province['name']}")
                        continue
                    print(f"{province['id']}. {province['name']}")
                province_id: str = input(f"Enter New Province ID or tap enter for skip (current: {data_of_manager['province_id']}): ")
                if province_id == "" or province_id.isspace():
                    province_id = data_of_manager['province_id']

                for type_ in types:
                    if type_["id"] == data_of_manager["type_id"]:
                        print(f"Current: {type_['id']}. {type_['name']}")
                        continue
                    print(f"{type_['id']}, {type_['name']}")
                new_type: str = input(f"Enter New Type ID or tap enter for skip (current: {data_of_manager['type_id']}): ")
                if new_type == "" or new_type.isspace():
                    new_type = data_of_manager["type_id"]

                queries = ("UPDATE users SET first_name=%s, last_name=%s, email=%s, phone_number=%s, province_id=%s,"
                           "type_id=%s WHERE id=%s")
                params = (first_name, last_name, email, phone_number, province_id, new_type, choice)
                execute_query(query=queries, params=params)
                print(success + "Manager information updated successfully.")
                return after_login_super()
        print(error + "Invalid Manager ID.")


def delete_manager():
    """
    Function to delete a manager.
    """
    while True:
        print(prints + "All Managers:")
        type_for_manager = execute_query(query="SELECT id FROM user_type WHERE name=%s", params=("Manager",), fetch="one")
        managers = execute_query(query="SELECT * FROM users WHERE type_id=%s", params=(type_for_manager[0],), fetch="all")
        if not managers:
            print(prints + "No Managers found.")
            return after_login_super()
        for manager in managers:
            print(f"{manager['id']}: {manager['first_name']} {manager['last_name']}")

        choice: str = input(enter + "Enter Manager ID to delete or stop for Exit: ")

        if choice == "stop":
            return after_login_super()

        for manager in managers:
            if int(choice) == manager["id"]:
                queries = "DELETE FROM users WHERE id=%s"
                params = (choice,)
                execute_query(queries, params)
                print(success + "Manager deleted successfully.")
                return after_login_super()
        print(error + "Invalid Manager ID.")


def add_manager_to_branch(manager_email: str=None):
    """
    Function to add a manager to a branch.
    """
    data_of_type = execute_query(query="SELECT * FROM user_type WHERE name=%s", params=("Manager",), fetch="one")
    if data_of_type is None:
        print(error + "No manager found.")
        return after_login_super()

    queries = "SELECT * FROM branch"
    data_of_branches = execute_query(query=queries, fetch="all")
    if not data_of_branches:
        print(error + "No Branches found.")
        return after_login_super()

    if manager_email is None:
        manager_email: str = input("Enter Manager Email: ")

    while not manager_email.endswith(email_details):
        print(error + "Invalid Manager Email enter stop for Exit")
        manager_email = input(re_enter + "Re-Enter: ")

        if manager_email.lower() == "stop":
            return after_login_super()

    queries = "SELECT * FROM users WHERE email=%s AND type_id=%s"
    params = (manager_email, data_of_type.get("id"))
    data_of_user = execute_query(query=queries, params=params, fetch="one")

    if data_of_user is None:
        print(error + "Manager not found.")
        return after_login_super()

    queries = "SELECT * FROM branch WHERE branch_manager_id=%s"
    params = (data_of_user.get("id"),)
    data_of_branch = execute_query(query=queries, params=params, fetch="one")

    if data_of_branch is not None:
        print(error + "This Manager Already Added To Another Branch.")
        return after_login_super()

    id_branch = []
    for branch in data_of_branches:
        print(f"{branch['id']}: {branch['name']}")
        id_branch.append(str(branch["id"]))

    branch_id: str = input("Enter Branch ID: ")
    while branch_id not in id_branch:
        print(error + "Invalid Branch ID stop for Exit")
        branch_id = input(re_enter + "Re-Enter: ")

        if branch_id.lower() == "stop":
            return after_login_super()

    queries = "UPDATE branch SET branch_manager_id = %s WHERE id = %s"
    params = (data_of_user.get("id"), int(branch_id))
    execute_query(query=queries, params=params)
    print(success + "Manager added successfully to the branch.")
    return after_login_super()


def remove_manager_from_branch():
    """
    Function to remove a manager from a branch.
    """
    data_of_type = execute_query(query="SELECT * FROM user_type WHERE name=%s", params=("Manager",), fetch="one")
    if data_of_type is None:
        print(error + "No manager found.")
        return after_login_super()

    queries = "SELECT * FROM branch"
    data_of_branches = execute_query(query=queries, fetch="all")
    if not data_of_branches:
        print(error + "No Branches found.")
        return after_login_super()

    view_all_managers(returning=False)
    manager_email: str = input("Enter Manager Email: ")

    while not manager_email.endswith(email_details):
        print(error + "Invalid Manager Email enter stop for Exit")
        manager_email = input(re_enter + "Re-Enter: ")

        if manager_email.lower() == "stop":
            return after_login_super()

    queries = "SELECT * FROM users WHERE email=%s AND type_id=%s"
    params = (manager_email, data_of_type.get("id"))
    data_of_user = execute_query(queries, params, fetch="one")
    if data_of_user is None:
        print(error + "Manager not found.")
        return after_login_super()

    queries = "SELECT * FROM branch WHERE branch_manager_id=%s"
    params = (data_of_user.get("id"),)
    data_of_branch = execute_query(query=queries, params=params, fetch="one")

    if data_of_branch is None:
        print(error + "This Manager is not assigned to any branch.")
        return after_login_super()

    queries = "UPDATE branch SET branch_manager_id = NULL WHERE id = %s"
    params = (data_of_branch.get("id"),)
    execute_query(query=queries, params=params)
    print(success + "Manager removed successfully from the branch.")
    return after_login_super()


def view_all_managers(returning: bool=True):
    """
    Function to view all managers.
    """
    data_of_type = execute_query(query="SELECT * FROM user_type WHERE name=%s", params=("Manager",), fetch="one")
    if data_of_type is None:
        print(error + "No manager found.")
        return after_login_super()

    queries = "SELECT * FROM users WHERE type_id=%s"
    params = (data_of_type.get("id"),)
    data_of_managers = execute_query(query=queries, params=params, fetch="all")
    if str(data_of_managers) == '[]':
        print(error + "No manager found.")
        return after_login_super()

    for manager in data_of_managers:
        print(f"ID: {manager['id']}\n"
              f"First Name: {manager['first_name']}\n"
              f"Last Name: {manager['last_name']}\n"
              f"Email: {manager['email']}\n"
              f"Phone Number: {manager['phone_number']}\n"
              f"Province ID: {manager['province_id']}\n"
              f"Password: {manager['password']}\n"
              f"Created At: {manager['created_at']}")
        print("-" * 20)
    if returning:
        return after_login_super()


def view_all_statistics_of_company():
    """
    Function to view all statistics of company.
    """
    data_of_type = execute_query(query="SELECT * FROM branch")
    if data_of_type is None:
        print(error + "No branch found.")
        return after_login_super()
    print("Statistics of Company")
    return after_login_super()


def view_all_statistics_of_one_branch():
    """
    Function to view all statistics of one branch.
    """
    data_of_type = execute_query(query="SELECT * FROM branch")
    if data_of_type is None:
        print(error + "No branch found.")
        return after_login_super()
    print("Statistics of One Branch")
    return after_login_super()


def view_all_cars_of_company():
    """
    Function to view all cars of company.
    """
    data_of_type = execute_query(query="SELECT * FROM branch")
    if data_of_type is None:
        print(error + "No branch found.")
        return after_login_super()
    queries = "SELECT * FROM car"
    data = execute_query(query=queries)
    for car in data:
        print(car)
        print("-------------------")

    return after_login_super()


def view_all_cars_of_one_branch():
    """
    Function to view all cars of one branch.
    """
    data_of_branch = execute_query(query="SELECT * FROM branch")
    if data_of_branch is None:
        print(error + "No branch found.")
        return after_login_super()

    data_of_cars = execute_query(query="SELECT * FROM car")
    if data_of_cars is None:
        print(error + "No car found.")
        return after_login_super()

    for branch in data_of_branch:
        print(branch)
        print("-------------------")

    branch_input: str = input("Enter branch ID or Name: ")
    while branch_input not in str(data_of_branch["id"]) and branch_input not in str(data_of_branch["name"]):
        print(error + "Invalid Branch ID or Name stop for Exit")
        branch_input = input(re_enter + "Re-Enter: ")

        if branch_input.lower() == "stop":
            return after_login_super()

    if branch_input.isdigit():
        branch_id = int(branch_input)
        data_of_branch = execute_query(query="SELECT * FROM branch WHERE id=%s", params=(branch_id,), fetch="one")
        if data_of_branch is None:
            print(error + "Branch not found.")
            return view_all_cars_of_one_branch()

    else:
        data_of_branch = execute_query(query="SELECT * FROM branch WHERE name=%s", params=(branch_input,), fetch="one")
        if data_of_branch is None:
            print(error + "Branch not found.")
            return view_all_cars_of_one_branch()

    data_of_cars_of_branch = execute_query("SELECT * FROM car WHERE branch_id=%s", (data_of_branch["id"],), "all")

    if data_of_cars_of_branch is None:
        print(error + "No car found in this branch.")
        return view_all_cars_of_one_branch()

    for car in data_of_cars_of_branch:
        print(car)
        print("-------------------")
    return after_login_super()


def after_login_super():
    """
    Function to handle after login as super admin.
    """
    print(command + "\n1. Create New Branch\n"
                    "2. Edit Branch Name\n"
                    "3. Delete Branch\n"
                    "4. View All Branches of Company\n"
                    "5. Create New Manager\n"
                    "6. Edit Manager Info\n"
                    "7. Delete Manager\n"
                    "8. Add Manager To Branch\n"
                    "9. Remove Manager From Branch\n"
                    "10. View All Managers of Company\n"
                    "11. View All Statistics of Company\n"
                    "12. View All Statistics of One Branch\n"
                    "13. View All CARS of Company\n"
                    "14. View All CARS of One Branch\n"
                    "15. LogOut\n")
    choice: str = input(enter + "Enter: ")

    if choice == "1":
        create_branch()

    elif choice == "2":
        edit_branch_name()

    elif choice == "3":
        delete_branch()

    elif choice == "4":
        view_all_branches()

    elif choice == "5":
        create_manager()

    elif choice == "6":
        edit_manager_info()

    elif choice == "7":
        delete_manager()

    elif choice == "8":
        add_manager_to_branch()

    elif choice == "9":
        remove_manager_from_branch()

    elif choice == "10":
        view_all_managers()

    elif choice == "11":
        view_all_statistics_of_company()

    elif choice == "12":
        view_all_statistics_of_one_branch()

    elif choice == "13":
        view_all_cars_of_company()

    elif choice == "14":
        view_all_cars_of_one_branch()

    elif choice == "15":
        print(success + "Logged out successfully.")
        return None

    else:
        print(error + "Invalid choice. Please try again.")
