from elmsdk import ELMSDK
import sys


def run_app(key, run_func):
    elm = ELMSDK(key, dev_mode=True)
    elm.setup_dev_run(run_func)

    avaliable_functions = ["add", "check_name", "exit"]
    while True:
        status = elm.begin_run()
        if status['func'] == "start":
            next_function = input(
                "Enter 'add' to add or update data, 'check_name' to get a number for a name or 'exit' to close: ")
            if next_function in avaliable_functions:
                status['func'] = next_function
                inputs = get_inputs(next_function)
                elm.end_run(message='Please input the following information',
                            continue_run={'func': next_function, 'inputs': inputs})
            else:
                elm.end_run(message='Invalid input', continue_run={'func': "start"})
        elif status['func'] == "exit":
            break
        elif status['func'] == 'add':
            # name, phone_number = ask_data()
            username = status["inputs"]["username"]
            phone_number = status["inputs"]["phone_number"]
            updates = []
            creates = []
            query = ['username', 'eq', username]
            data_ob = elm.db_read(1, query)

            if data_ob:
                update = {'phone_number': phone_number}
                updates.append({'table': 1, 'query': query, "is_global": False, "update": update})
            else:
                to_add = {'username': username, 'phone_number': phone_number}
                creates.append(dict(table=1, is_global=False, data=to_add))
            elm.end_run(message='Your information has been saved', continue_run={'func': "start"}, db_updates=updates,
                        db_creates=creates)
        elif status['func'] == 'check_name':
            username = status["inputs"]["username"]
            data = elm.db_read(1, ['username', 'eq', username], limit=3)
            try:
                print(data[0]['phone_number'])
            except:
                print("No records")
            elm.end_run(message='Name checked', continue_run={'func': "start"})


# def ask_username():
#     username = input("Please input name: ")
#     return username
#
#
# def ask_data():
#     username = ask_username()
#     phone_number = input("Please input phone number: ")
#     return username, phone_number


def get_inputs(func):
    if func == "add":
        inputs = get_add_inputs()
    elif func == "check_name":
        inputs = get_check_inputs()
    else:
        inputs = get_exit_inputs()
    return inputs


def get_add_inputs():
    inputs = [{
        'name': 'username'
    }, {
        'name': 'phone_number',
    }]
    return inputs


def get_check_inputs():
    inputs = [{
        'name': 'username'
    }]
    return inputs


def get_exit_inputs():
    inputs = []
    return inputs


if __name__ == '__main__':
    run_app(sys.argv[1], sys.argv[2])
