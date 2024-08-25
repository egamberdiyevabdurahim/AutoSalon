from for_print import error, enter, success, prints, command, re_enter

from db_settings import Database, execute_query

from .addition import email_details, phone_details


def create_shopper(email_of_manager: str):
    """
    Function to create a new shopper.
    """
    first_name: str = input("Enter First Name: ")
    while not first_name.isalpha():
        print(error + "Invalid First Name enter stop for Exit")
        first_name = input(re_enter + "Re-Enter: ")

        if first_name.lower() == "stop":
            return after_login_admin()

    last_name: str = input("Enter Last Name: ")
    while not last_name.isalpha():
        print(error + "Invalid Last Name enter stop for Exit")
        last_name = input(re_enter + "Re-Enter: ")

        if last_name.lower() == "stop":
            return after_login_admin()

    email: str = input("Enter Email: ")
    while not email.endswith(email_details):
        print(error + "Invalid Email enter stop for Exit")
        email = input(re_enter + "Re-Enter: ")

        if email.lower() == "stop":
            return after_login_admin()

    phone_number: str = input("Enter Phone Number: ")
    while not phone_number.startswith(phone_details):
        print(error + "Invalid Phone Number enter stop for Exit")
        phone_number = input(re_enter + "Re-Enter: ")

        if phone_number.lower() == "stop":
            return after_login_admin()

    queries_province = "SELECT * FROM province"
    data = execute_query(query=queries_province, fetch="all")
    datas = []
    for column in data:
        print(f"{column[0]}: {column[1]}")
        datas.append(column[0])

    province_id: str = input("Enter Province ID: ")
    while province_id not in str(datas):
        print(error + "Invalid Province ID enter stop for Exit")
        province_id = input(re_enter + "Re-Enter: ")

        if province_id.lower() == "stop":
            return after_login_admin()

    password: str = input("Enter New Password: ")
    while len(password) < 8:
        print(error + "Password must be at least 8 characters long.\n"
                      "stop for Exit")
        password = input(re_enter + "Re-Enter password: ")
        if password.lower() == "stop":
            return after_login_admin()

    types = execute_query("SELECT * FROM user_type WHERE name=%s", ("Shopper",), "one")

    try:
        queries = "INSERT INTO users (first_name, last_name, email, phone_number, password, province_id, type_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        params = (first_name, last_name, email, phone_number, password, int(province_id), int(types.get("id")))
        execute_query(query=queries, params=params)
        # Add shopper to shop assistant table if the user type is shopper
        user_data = execute_query(query="SELECT * FROM users WHERE email=%s", params=(email,), fetch="one")
        execute_query(query="INSERT INTO shop_assistant (user_id) VALUES (%s)", params=(user_data.get("id"),))
        print(success + "New Shopper created successfully.")
        choice_for_branching: str = input("Do you want to add this shopper to your branch(y/n): ")
    except Exception as e:
        print(error + str(e))
        return after_login_admin()
    if choice_for_branching.lower() == "y":
        return add_shopper_to_branch(email_of_manager, created_data=user_data['id'])
    return after_login_admin()


def edit_shopper_info():
    """
    Function to edit shopper info.
    """
    print(prints + "All Shoppers:")
    shoppers = execute_query(query="SELECT id, first_name, last_name FROM users WHERE type_id = %s",
                             params=(execute_query("SELECT * FROM user_type WHERE name=%s",
                                                   ("Shopper",), "one").get("id"),), fetch="all")
    if not shoppers:
        print(error + "No Shoppers found.")
        return after_login_admin()

    for shopper in shoppers:
        print(f"{shopper[0]}: {shopper[1]} {shopper[2]}")

    shopper_id: str = input("Enter Shopper ID: ")
    while not shopper_id.isdigit() or int(shopper_id) not in [shopper[0] for shopper in shoppers]:
        print(error + "Invalid Shopper ID enter stop for Exit")
        shopper_id = input(re_enter + "Re-Enter: ")
        if shopper_id.lower() == "stop":
            return after_login_admin()

    while True:
        shopper_data = execute_query(query="SELECT * FROM users WHERE id=%s", params=(shopper_id,), fetch="one")
        print(f"Current Shopper Details:")
        print(f"ID: {shopper_data.get('id')}"
              f"\nFirst Name: {shopper_data.get('first_name')}"
              f"\nLast Name: {shopper_data.get('last_name')}"
              f"\nEmail: {shopper_data.get('email')}"
              f"\nPhone Number: {shopper_data.get('phone_number')}"
              f"\nPassword: {shopper_data.get('password')}"
              f"\nProvince: {execute_query('SELECT name FROM province WHERE id=%s', (shopper_data.get('province_id'),), fetch='one').get('name')}"
              f"\nCreated At: {shopper_data.get('created_at')}")
        print(command + "\n"
                        "1. Edit First Name\n"
                        "2. Edit Last Name\n"
                        "3. Edit Email\n"
                        "4. Edit Phone Number\n"
                        "5. Edit Password\n"
                        "6. Edit Province\n"
                        "7. Exit")
        choice: str = input(enter + "Enter: ")
        if choice == "1":
            new_first_name: str = input("Enter New First Name: ")
            while not new_first_name.isalpha():
                print(error + "Invalid First Name enter stop for Exit")
                new_first_name = input(re_enter + "Re-Enter: ")
                if new_first_name.lower() == "stop":
                    return after_login_admin()
            execute_query(query="UPDATE users SET first_name=%s WHERE id=%s", params=(new_first_name, shopper_id))
            print(success + "First Name updated successfully.")

        elif choice == "2":
            new_last_name: str = input("Enter New Last Name: ")
            while not new_last_name.isalpha():
                print(error + "Invalid Last Name enter stop for Exit")
                new_last_name = input(re_enter + "Re-Enter: ")
                if new_last_name.lower() == "stop":
                    return after_login_admin()
            execute_query(query="UPDATE users SET last_name=%s WHERE id=%s", params=(new_last_name, shopper_id))
            print(success + "Last Name updated successfully.")

        elif choice == "3":
            new_email: str = input("Enter New Email: ")
            while not new_email.endswith(email_details):
                print(error + "Invalid Email enter stop for Exit")
                new_email = input(re_enter + "Re-Enter: ")
                if new_email.lower() == "stop":
                    return after_login_admin()
            execute_query(query="UPDATE users SET email=%s WHERE id=%s", params=(new_email, shopper_id))
            print(success + "Email updated successfully.")

        elif choice == "4":
            new_phone_number: str = input("Enter New Phone Number: ")
            while not new_phone_number.startswith(phone_details):
                print(error + "Invalid Phone Number enter stop for Exit")
                new_phone_number = input(re_enter + "Re-Enter: ")
                if new_phone_number.lower() == "stop":
                    return after_login_admin()
            execute_query(query="UPDATE users SET phone_number=%s WHERE id=%s", params=(new_phone_number, shopper_id))
            print(success + "Phone Number updated successfully.")

        elif choice == "5":
            new_password: str = input("Enter New Password: ")
            while len(new_password) < 8:
                print(error + "Password must be at least 8 characters long.\n"
                      "stop for Exit")
                new_password = input(re_enter + "Re-Enter password: ")
                if new_password.lower() == "stop":
                    return after_login_admin()
            execute_query(query="UPDATE users SET password=%s WHERE id=%s", params=(new_password, shopper_id))
            print(success + "Password updated successfully.")

        elif choice == "6":
            provinces = execute_query(query="SELECT * FROM province", fetch="all")
            for province in provinces:
                if province["id"] == shopper_data['province_id']:
                    print(f"Current: {province['id']}. {province['name']}")
                    continue
                print(f"{province['id']}. {province['name']}")
            new_province_id: str = input("Enter New Province ID: ")
            while not new_province_id.isdigit() or int(new_province_id) not in [province[0] for province in execute_query("SELECT id FROM province", fetch="all")]:
                print(error + "Invalid Province ID enter stop for Exit")
                new_province_id = input(re_enter + "Re-Enter: ")
                if new_province_id.lower() == "stop":
                    return after_login_admin()

            execute_query(query="UPDATE users SET province_id=%s WHERE id=%s", params=(new_province_id, shopper_id))
            print(success + "Province updated successfully.")

        elif choice == "7":
            print(success + "Exiting...")
            return after_login_admin()

        else:
            print(error + "Invalid choice, try again.")


def delete_shopper():
    """
    Function to delete shopper.
    """
    print(prints + "All Shoppers:")
    shoppers = execute_query(query="SELECT id, first_name, last_name FROM users WHERE type_id = %s",
                             params=(execute_query("SELECT * FROM user_type WHERE name=%s",
                                                   ("Shopper",), "one").get("id"),), fetch="all")
    if not shoppers:
        print(error + "No Shoppers found.")
        return after_login_admin()

    for shopper in shoppers:
        print(f"{shopper[0]}: {shopper[1]} {shopper[2]}")

    shopper_id: str = input("Enter Shopper ID: ")
    while not shopper_id.isdigit() or int(shopper_id) not in [shopper[0] for shopper in shoppers]:
        print(error + "Invalid Shopper ID enter stop for Exit")
        shopper_id = input("Re-Enter: ")

        if shopper_id.lower() == "stop":
            return after_login_admin()

    execute_query(query="DELETE FROM shop_assistant WHERE user_id=%s", params=(shopper_id,))
    execute_query(query="DELETE FROM users WHERE id=%s", params=(shopper_id,))
    print(success + "Shopper deleted successfully.")
    return after_login_admin()


def add_shopper_to_branch(email: str, created_data: str=None):
    """
    Function to add shopper to branch.
    """
    manager_data = execute_query(query="SELECT * FROM users WHERE email=%s",
                                 params=(email,), fetch="one")

    branch_data = execute_query(query="SELECT * FROM branch WHERE branch_manager_id=%s", params=(manager_data[0],), fetch="one")

    if created_data is None:
        shoppers_in = execute_query(query="SELECT * FROM users WHERE type_id = %s",
                                    params=(execute_query("SELECT * FROM user_type WHERE name=%s",
                                                          ("Shopper",), "one").get("id"),), fetch="all")
        if not shoppers_in:
            print(error + "No Shoppers found.")
            return after_login_admin()

        dict_for_shoppers = {}
        for shopper in shoppers_in:
            shoppers = execute_query(query="SELECT id, user_id FROM shop_assistant WHERE user_id=%s AND branch_id is null",
                                     params=(shopper[0],), fetch="one")
            if shoppers:
                dict_for_shoppers[str(shoppers[1])] = shoppers[0]

        if not dict_for_shoppers:
            print(error + "No Unemployed Shoppers found.")
            return after_login_admin()

        for shopper in shoppers_in:
            if str(shopper["id"]) in list(dict_for_shoppers.keys()):
                print(f"{dict_for_shoppers[str(shopper.get('id'))]}: {shopper.get('first_name')} {shopper.get('last_name')}")

        shopper_id: str = input("Enter Shopper ID: ")
        while not shopper_id.isdigit() or int(shopper_id) not in list(dict_for_shoppers.values()):
            print(error + "Invalid Shopper ID enter stop for Exit")
            shopper_id = input("Re-Enter: ")

            if shopper_id.lower() == "stop":
                return after_login_admin()

    else:
        shoppers = execute_query(query="SELECT id FROM shop_assistant WHERE user_id=%s",
                                 params=(created_data,), fetch="one")
        shopper_id = shoppers.get("id")

    execute_query(query="UPDATE shop_assistant SET branch_id=%s WHERE id=%s", params=(branch_data.get("id"), shopper_id))
    print(success + "Shopper added to your Branch successfully.")
    return after_login_admin()


def remove_shopper_from_branch(email: str):
    """
    Function to remove shopper from branch.
    """
    manager_data = execute_query(query="SELECT * FROM users WHERE email=%s",
                                 params=(email,), fetch="one")

    branch_data = execute_query(query="SELECT * FROM branch WHERE branch_manager_id=%s", params=(manager_data["id"],), fetch="one")

    shoppers_in = execute_query(query="SELECT * FROM users WHERE type_id = %s",
                                params=(execute_query("SELECT * FROM user_type WHERE name=%s",
                                                      ("Shopper",), "one").get("id"),), fetch="all")
    if not shoppers_in:
        print(error + "No Shoppers found.")
        return after_login_admin()

    dict_for_shoppers = {}
    for shopper in shoppers_in:
        shoppers = execute_query(query="SELECT id, user_id FROM shop_assistant WHERE user_id=%s AND branch_id=%s",
                                 params=(shopper[0], branch_data.get("id")), fetch="one")
        if shoppers:
            dict_for_shoppers[str(shoppers[1])] = shoppers[0]

    if not dict_for_shoppers:
        print(error + "No Shoppers Found Of Your Branch.")
        return after_login_admin()

    for shopper in shoppers_in:
        if str(shopper.get("id")) in list(dict_for_shoppers.keys()):
            print(f"{dict_for_shoppers[str(shopper.get('id'))]}: {shopper.get('first_name')} {shopper.get('last_name')}")

    shopper_id: str = input("Enter Shopper ID: ")
    while not shopper_id.isdigit() or int(shopper_id) not in list(dict_for_shoppers.values()):
        print(error + "Invalid Shopper ID enter stop for Exit")
        shopper_id = input("Re-Enter: ")

        if shopper_id.lower() == "stop":
            return after_login_admin()

    execute_query(query="UPDATE shop_assistant SET branch_id=%s WHERE id=%s", params=(None, shopper_id))
    print(success + "Shopper removed from your Branch successfully.")
    return after_login_admin()


def view_all_shoppers_in_branch(email: str):
    """
    Function to view all shoppers in branch.
    """
    manager_data = execute_query(query="SELECT * FROM users WHERE email=%s",
                                 params=(email,), fetch="one")

    branch_data = execute_query(query="SELECT * FROM branch WHERE branch_manager_id=%s", params=(manager_data.get("id"),), fetch="one")

    shoppers_in = execute_query(query="SELECT * FROM users WHERE type_id = %s",
                                params=(execute_query("SELECT * FROM user_type WHERE name=%s",
                                                      ("Shopper",), "one").get("id"),), fetch="all")
    if not shoppers_in:
        print(error + "No Shoppers found.")
        return after_login_admin()

    dict_for_shoppers = {}
    for shopper in shoppers_in:
        shoppers = execute_query(query="SELECT id, user_id FROM shop_assistant WHERE user_id=%s AND branch_id=%s",
                                 params=(shopper[0], branch_data['id']), fetch="one")
        if shoppers:
            dict_for_shoppers[str(shoppers['user_id'])] = shoppers["id"]

    if not dict_for_shoppers:
        print(error + "No Shoppers found in Your Branch.")
        return after_login_admin()

    for shopper in shoppers_in:
        if str(shopper.get("id")) in list(dict_for_shoppers.keys()):
            print(f"Shopper ID in users table: {shopper['id']}\n"
                  f"    First Name: {shopper['first_name']}\n"
                  f"    Last Name: {shopper['last_name']}\n"
                  f"    Email: {shopper['email']}\n"
                  f"    Phone Number: {shopper['phone_number']}\n"
                  f"    Password: {shopper['password']}\n"
                  f"    User Type: {execute_query('SELECT * FROM user_type WHERE id=%s', (shopper['type_id'],), fetch='one')['name']}\n"
                  f"    Province: {execute_query('SELECT * FROM province WHERE id=%s', (shopper['province_id'],), fetch='one')['name']}\n"
                  f"    ID in shop_assistant table: {dict_for_shoppers[str(shopper['id'])]}\n"
                  f"        Branch ID: {branch_data['id']}\n"
                  f"        Branch Name: {branch_data['name']}\n"
                  )
            print("-"*20)
    return after_login_admin()


def create_car(email: str):
    """
    Function to create new car.
    """
    manager_data = execute_query(query="SELECT * FROM users WHERE email=%s", params=(email,), fetch="one")

    if not manager_data:
        print("Manager data not found for the given email.")
        return after_login_admin()

    branch_data = execute_query(query="SELECT * FROM branch WHERE branch_manager_id=%s",
                                params=(manager_data.get("id"),), fetch="one")

    if not branch_data:
        print("Branch data not found for the manager.")
        return after_login_admin()

    brand_data = execute_query(query="SELECT * FROM brand", fetch="all")

    model_data = execute_query(query="SELECT * FROM model", fetch="all")

    type_data = execute_query(query="SELECT * FROM type", fetch="all")

    color_data = execute_query(query="SELECT * FROM color", fetch="all")

    for brand in brand_data:
        for model in model_data:
            if model["brand_id"] == brand["id"]:
                print(f"{model['id']}: {brand['name']}/{model['name']}")

    choice_model: str = input("Enter Model ID: ")
    while not choice_model.isdigit() or int(choice_model) not in [model["id"] for model in model_data]:
        print(error + "Invalid Model ID enter stop for Exit")
        choice_model = input("Re-Enter: ")

        if choice_model.lower() == "stop":
            return after_login_admin()

    year: str = input("Created Year: ")
    while not year.isdigit() or int(year) < 2020:
        print("Invalid Year enter stop for Exit")
        year = input("Re-Enter: ")

        if year.lower() == "stop":
            return after_login_admin()

    for type_ in type_data:
        print(f"{type_['id']}: {type_['name']}")

    choice_type: str = input("Enter Type ID: ")
    while not choice_type.isdigit() or int(choice_type) not in [type_["id"] for type_ in type_data]:
        print(error + "Invalid Type ID enter stop for Exit")
        choice_type = input("Re-Enter: ")

        if choice_type.lower() == "stop":
            return after_login_admin()

    for color_ in color_data:
        print(f"{color_['id']}: {color_['name']}")

    color: str = input("Enter Color ID: ")
    while not color.isdigit() or int(color) not in [color_["id"] for color_ in color_data]:
        print(error + "Invalid Color ID enter stop for Exit")
        color = input("Re-Enter: ")

        if color.lower() == "stop":
            return after_login_admin()

    price: str = input("Enter price: ")
    while not price.isdigit() and float(price) <= 0.0:
        print(error + "Invalid price enter stop for Exit")
        price = input("Re-Enter: ")

        if price.lower() == "stop":
            return after_login_admin()

    execute_query(query="INSERT INTO car (branch_id, model_id, year, type_id, color_id, price) VALUES (%s, %s, %s, %s, %s, %s)",
                  params=(branch_data["id"], choice_model, f"01-01-{year}", choice_type, color, float(price)))
    print(success + "Car added to your Branch successfully.")
    return after_login_admin()


def delete_car(email: str):
    """
    Function to delete car.
    """
    manager_data = execute_query(query="SELECT * FROM users WHERE email=%s",
                                 params=(email,), fetch="one")

    branch_data = execute_query(query="SELECT * FROM branch WHERE branch_manager_id=%s", params=(manager_data.get("id"),), fetch="one")

    car_data = execute_query(query="SELECT * FROM car WHERE branch_id=%s", params=(branch_data["id"],), fetch="all")

    if not car_data:
        print(error + "No Cars found in Your Branch.")
        return after_login_admin()

    for car in car_data:
        print(f"Car ID: {car['id']}\n"
              f"    Model: {execute_query('SELECT * FROM model WHERE id=%s', (car['model_id'],), fetch='one')['name']}\n"
              f"    Year: {car['year']}\n"
              f"    Type: {execute_query('SELECT * FROM type WHERE id=%s', (car['type_id'],), fetch='one')['name']}\n"
              f"    Color: {execute_query('SELECT * FROM color WHERE id=%s', (car['color_id'],), fetch='one')['name']}\n"
              f"    Price: {car['price']}\n"
              f"    Created At: {car['created_at']}"
              )
        print("-"*20)

    choice_car: str = input("Enter Car ID to Delete: ")
    while not choice_car.isdigit() or int(choice_car) not in [car["id"] for car in car_data]:
        print(error + "Invalid Car ID enter stop for Exit")
        choice_car = input("Re-Enter: ")

        if choice_car.lower() == "stop":
            return after_login_admin()

    execute_query(query="DELETE FROM car WHERE id=%s", params=(choice_car,))
    print(success + "Car deleted from your Branch successfully.")
    return after_login_admin()


def edit_car_price(email: str):
    """
    Function to edit car price.
    """
    manager_data = execute_query(query="SELECT * FROM users WHERE email=%s",
                                 params=(email,), fetch="one")

    branch_data = execute_query(query="SELECT * FROM branch WHERE branch_manager_id=%s", params=(manager_data.get("id"),), fetch="one")

    car_data = execute_query(query="SELECT * FROM car WHERE branch_id=%s", params=(branch_data["id"],), fetch="all")

    if not car_data:
        print(error + "No Cars found in Your Branch.")
        return after_login_admin()

    for car in car_data:
        print(f"Car ID: {car['id']}\n"
              f"    Model: {execute_query('SELECT * FROM model WHERE id=%s', (car['model_id'],), fetch='one')['name']}\n"
              f"    Year: {car['year']}\n"
              f"    Type: {execute_query('SELECT * FROM type WHERE id=%s', (car['type_id'],), fetch='one')['name']}\n"
              f"    Color: {execute_query('SELECT * FROM color WHERE id=%s', (car['color_id'],), fetch='one')['name']}\n"
              f"    Price: {car['price']}\n"
              f"    Created At: {car['created_at']}"
              )
        print("-"*20)

    choice_car: str = input("Enter Car ID to Edit Price: ")
    while not choice_car.isdigit() or int(choice_car) not in [car["id"] for car in car_data]:
        print(error + "Invalid Car ID enter stop for Exit")
        choice_car = input("Re-Enter: ")

        if choice_car.lower() == "stop":
            return after_login_admin()

    new_price: str = input("Enter New Price: ")
    while not new_price.isdigit() or float(new_price) <= 0.0:
        print(error + "Invalid Price enter stop for Exit")
        new_price = input("Re-Enter: ")

        if new_price.lower() == "stop":
            return after_login_admin()

    execute_query(query="UPDATE car SET price=%s WHERE id=%s", params=(float(new_price), choice_car))
    print(success + "Price updated successfully.")
    return after_login_admin()


def view_all_cars(email: str):
    """
    Function to view all cars.
    """
    manager_data = execute_query(query="SELECT * FROM users WHERE email=%s",
                                 params=(email,), fetch="one")

    branch_data = execute_query(query="SELECT * FROM branch WHERE branch_manager_id=%s", params=(manager_data.get("id"),), fetch="one")

    car_data = execute_query(query="SELECT * FROM car WHERE branch_id=%s", params=(branch_data["id"],), fetch="all")

    if not car_data:
        print(error + "No Cars found in Your Branch.")
        return after_login_admin()

    for car in car_data:
        print(f"Car ID: {car['id']}\n"
              f"    Model: {execute_query('SELECT * FROM model WHERE id=%s', (car['model_id'],), fetch='one')['name']}\n"
              f"    Year: {car['year']}\n"
              f"    Type: {execute_query('SELECT * FROM type WHERE id=%s', (car['type_id'],), fetch='one')['name']}\n"
              f"    Color: {execute_query('SELECT * FROM color WHERE id=%s', (car['color_id'],), fetch='one')['name']}\n"
              f"    Price: {car['price']}\n"
              f"    Created At: {car['created_at']}"
              )
        print("-"*20)

    return after_login_admin()


def view_all_statistics(email: str):
    """
    Function to view all statistics.
    """
    print("All statistics")
    print("Statistics will be displayed here.")
    return after_login_admin()


def after_login_admin(email: str=None):
    """
    Function to handle after login as admin.
    """
    print(success + "Welcome, Admin!")
    while True:
        print(command + "\n"
                        "1. Create New Shopper\n"
                        "2. Edit Shopper Info\n"
                        "3. Delete Shopper\n"
                        "4. Add Shopper to your Branch\n"
                        "5. Remove Shopper from your Branch\n"
                        "6. View All Shoppers In Your Branch\n"
                        "7. Add New CAR to your Branch\n"
                        "8. Delete CAR from your Branch\n"
                        "9. Edit Price of CAR in your Branch\n"
                        "10. View All CARS in your Branch\n"
                        "11. View All Statistics of your Branch\n"
                        "12. LogOut\n")
        choice: str = input(enter + "Enter: ")

        if choice == "1":
            # Create New Shopper
            create_shopper(email)

        elif choice == "2":
            # Edit Shopper Info
            edit_shopper_info()

        elif choice == "3":
            # Delete Shopper
            delete_shopper()

        elif choice == "4":
            # Add Shopper to your Branch
            add_shopper_to_branch(email)

        elif choice == "5":
            # Remove Shopper from your Branch
            remove_shopper_from_branch(email)

        elif choice == "6":
            # View All Shoppers In Your Branch
            view_all_shoppers_in_branch(email)

        elif choice == "7":
            # Add New CAR to your Branch
            create_car(email)

        elif choice == "8":
            # Delete CAR from your Branch
            delete_car(email)

        elif choice == "9":
            # Edit Price of CAR in your Branch
            edit_car_price(email)

        elif choice == "10":
            # View All CARS in your Branch
            view_all_cars(email)

        elif choice == "11":
            # View All Statistics of your Branch
            view_all_statistics(email)

        elif choice == "12":
            # LogOut
            print(success + "Exiting...")
            break
