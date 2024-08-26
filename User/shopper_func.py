from ..db_settings import execute_query
from ..for_print import enter, success,  command


def create_contract(email):
    # Retrieve user information by email
    shop_assistant = execute_query("SELECT * FROM users WHERE email=%s", (email,), "one")
    shop_assistant_id = shop_assistant.get("id")

    # Fetch car and its model and brand details
    cars = execute_query("SELECT * FROM cars", fetch="all")

    for car in cars:
        status = car.get("status")
        if status:

            car_id = (car.get("car_id"),)

            model_id = (car.get("model_id"),)

            car_model = execute_query("SELECT * FROM models WHERE id=%s", params=model_id, fetch="one")

            brand_id = (car_model.get("brand_id"),)

            car_brand = execute_query("SELECT * FROM brands WHERE id=%s", params=brand_id, fetch="one")

            car_color_id = (car.get("color_id"),)

            car_color = execute_query("SELECT * FROM colors WHERE id=%s", params=car_color_id, fetch="one")

            car_t_id = (car.get("type_id"),)

            car_type = execute_query("SELECT * FROM types WHERE id=%s", params=car_t_id, fetch="one")

            car_b_id = (car.get("branch_id"),)

            car_branch = execute_query("SELECT * FROM branches WHERE id=%s", params=car_b_id, fetch="one")

            year = car.get("year")

            price = car.get("price")

            print(f"\nCar id: {car_id}\n"
                  
                  f"Car Brand: {car_brand[1]}\n"
        
                  f"Car model: {car_model[1]}\n"
        
                  f"Car id: {car_id}\n"
                  
                  f"Car color: {car_color[1]}\n"
                  
                  f"Car type: {car_type[1]}\n"
                  
                  f"Car branch: {car_branch}\n"
                  
                  f"Year: {year}\n"
                  
                  f"Price: {price}")

    # Input the car and user IDs
    car_id = input("Enter car id: ")
    user_id = input("Enter user_id: ")

    # Create a new contract
    queries = "INSERT INTO contracts (shop_assistant_id, car_id, user_id) VALUES (%s, %s, %s)"
    params = (shop_assistant_id, car_id, user_id)
    execute_query(query=queries, params=params)

    return after_login_shopper(email)


def show_all_my_contracts(email):
    # Get user data based on the provided email

    user_db = execute_query(query="SELECT * FROM users WHERE email=%s", params=(email,), fetch="one")

    user_id = (user_db.get("id"))

    # Retrieve all contracts associated with the user

    contracts = execute_query("SELECT * FROM contracts WHERE user_id=%s", params=user_id, fetch="all")

    for contract in contracts:
        contract_id = contract.get("id")

        user_id = (contract.get("id"),)

        # Fetch user data from users table

        user_db = execute_query("SELECT * FROM users WHERE id=%s", params=user_id, fetch="one")

        created_at = (contract.get("created_at"),)

        # Fetch shop assistant data

        shop_assistant_id = (contract.get("shop_assistant_id"),)

        shop_assistant_db = execute_query("SELECT * FROM shop_assistant WHERE id=%s", params=shop_assistant_id,
                                          fetch="one")

        sh_a_user_id = (shop_assistant_db.get("user_id"),)

        # Fetch the shop assistant's user data

        sh_user_db = execute_query("SELECT * FROM users WHERE id=%s", params=sh_a_user_id, fetch="one")

        # Fetch car and its model and brand details

        car_id = (contract.get("car_id"),)

        car_db = execute_query("SELECT * FROM cars WHERE id=%s", params=car_id, fetch="one")

        model_id = (car_db.get("model_id"),)

        car_model = execute_query("SELECT * FROM models WHERE id=%s", params=model_id, fetch="one")

        brand_id = (car_model.get("brand_id"),)

        car_brand = execute_query("SELECT * FROM brands WHERE id=%s", params=brand_id, fetch="one")

        # Print the contract details

        print(f"\nContract id: {contract_id}\n"

              f"Shopper name: {sh_user_db[1]}\n"

              f"Car Brand: {car_brand[1]}\n"

              f"Car model: {car_model[1]}\n"

              f"Car id: {car_id}\n"

              f"User name: {user_db[1]}\n"

              f"User id: {user_id}\n"

              f"Time when the contract was concluded: {created_at}")

    return after_login_shopper(email)


def show_all_my_payment_statuses(email):
    # Retrieve user information by email
    user = execute_query("SELECT * FROM users WHERE email=%s", (email,), "one")
    user_id = user.get("id")

    # Retrieve shop assistant information
    shop_assistant = execute_query("SELECT * FROM shop_assistant WHERE user_id=%s", (user_id,), fetch="one")
    shop_assistant_id = shop_assistant.get("id")

    # Retrieve all contracts belonging to the user
    my_contracts = execute_query("SELECT * FROM contracts WHERE shop_assistant_id=%s", (shop_assistant_id,),
                                 fetch="all")

    # Display installment payment statuses for each contract
    for contract in my_contracts:
        contract_id = contract.get("id")

        user_id = contract.get("user_id")
        user_db = execute_query("SELECT * FROM users WHERE id=%s", params=user_id, fetch="one")

        installments = execute_query("SELECT * FROM installments WHERE contracts_id=%s", (contract_id,), fetch="all")
        for installment in installments:
            i_id = installment.get("id")
            amount = installment.get("amount")
            paid = installment.get("paid")
            deadline = installment("deadline")
            created_at = installment("created_at")
            print(f"\nInstallment id: {i_id}\n"
                  f"{user_db[1]} and his id {id}, can pay {amount} payment until {deadline} period,"
                  f" so far he has paid {paid}."
                  f"Date of contract: {created_at}\n")

    return after_login_shopper(email)


def after_login_shopper(email):
    """
    Function to handle after login as user.
    """
    print(success + "Welcome !")
    while True:
        print(command + "\n.1  Create New Contract\n"
                        "2. Show All My Contracts\n"
                        "3. Show All My Payment Statuses\n"
                        "4. Logout\n")
        choice: str = input(enter + "Enter: ")

        if choice == "1":
            create_contract(email)

        elif choice == "2":
            show_all_my_contracts(email)

        elif choice == "3":
            show_all_my_payment_statuses(email)

        elif choice == "4":
            print(success + "Logged out successfully.")
            return None
