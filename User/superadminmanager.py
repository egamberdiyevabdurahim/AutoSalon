from datetime import datetime
from jsonfilemanager import JSONFIleManager

filename = './data/branches.json'




def create_branch(branch_name):
    try:
        data = JSONFIleManager(filename).load_data()
        data.append({
            'branch_name': branch_name,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        JSONFIleManager(filename).save_data(data)
        return True
    except Exception as e:
        return False

def create_manager(first_name, last_name, email, phone_number, password,):
    try:
        data = JSONFIleManager(filename).load_data()
        data.append({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phone_number,
            'password': password,
        })


