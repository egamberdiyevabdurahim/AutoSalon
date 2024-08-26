from ..db_settings import execute_query
from ..for_print import enter, success, command


def after_login_user(email):
    """
    Function to handle after login as user.
    """
    print(success + "Welcome !")
    while True:
        print(command + "\n1.  Show All My Data\n"
                        "2. Show All My Contracts\n"
                        "3. Show All My Debt\n"
                        "4. Show All My Payment Statuses\n"
                        "5. Logout\n")
        choice: str = input(enter + "Enter: ")

        if choice == "1":
            user_db = execute_query(query="SELECT * FROM users WHERE email=%s", params=(email,), fetch="one")
            print(user_db)
            after_login_user(email)

        elif choice == "2":

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

                print(f"Contract id: {contract_id}\n"

                      f"Shopper name: {sh_user_db[1]}\n"

                      f"Car Brand: {car_brand[1]}\n"

                      f"Car model: {car_model[1]}\n"

                      f"Car id: {car_id}\n"

                      f"User name: {user_db[1]}\n"

                      f"User id: {user_id}\n"

                      f"Time when the contract was concluded: {created_at}")

        elif choice == "3":
            user_db = execute_query(query="SELECT * FROM users WHERE email=%s", params=(email,), fetch="one")
            user_id = (user_db.get("id"))
            contracts = execute_query("SELECT * FROM contracts WHERE user_id=%s", params=user_id, fetch="all")
            for contract in contracts:
                contract_id = (contract.get("id"),)
                installment = execute_query("SELECT * FROM installments WHERE selling_id=%s", params=contract_id,
                                            fetch="one")
                amount = installment.get("amount")
                paid = installment.get("paid")
                if amount < paid:
                    print(f"Debt: {amount - paid} , {installment}")
                elif amount == paid:
                    print(f"This fee has been successfully paid: {installment}")
        elif choice == "4":
            # Retrieve user information by email
            user = execute_query("SELECT * FROM users WHERE email=%s", (email,), "one")
            user_id = user.get("id")

            # Retrieve all contracts belonging to the user
            my_contracts = execute_query("SELECT * FROM contracts WHERE user_id=%s", (user_id,),
                                         fetch="all")
            # Display installment payment statuses for each contract
            for contract in my_contracts:
                contract_id = contract.get("id")
                installments = execute_query("SELECT * FROM installments WHERE contracts_id=%s", (contract_id,),
                                             fetch="all")
                for installment in installments:
                    i_id = installment.get("id")
                    amount = installment.get("amount")
                    paid = installment.get("paid")
                    deadline = installment("deadline")
                    created_at = installment("created_at")
                    print(f"\nInstallment id: {i_id}\n"
                          f"You can request {amount} payment until {deadline} time, you have already paid {paid}.\n"
                          f"Date of contract: {created_at}\n")

        elif choice == "5":
            print(success + "Logged out successfully.")
