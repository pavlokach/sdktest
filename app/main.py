from elmsdk import ELMSDK


def run_app():
    key = input("Enter dev key: ")
    elm = ELMSDK(key, dev_mode=True)

    while True:
        elm.setup_dev_run("add")
        status = elm.begin_run()
        next_function = input(
            "Enter 'add' to add or update data, 'check_name' to get a number for a name or 'exit' to close: ")
        status['func'] = next_function
        if status['func'] == 'exit':
            break
        elif status['func'] == 'add':
            # chosen = {'vehicle': "BMW", 'color': "Red"}
            name, phone_number = ask_data()

            updates = []
            creates = []
            query = ['name', 'eq', name]
            data_ob = elm.db_read(1, query)

            if data_ob:
                update = {'phone_number': phone_number}
                updates.append({'table': 1, 'query': query, "is_global": False, "update": update})
            else:
                to_add = {'name': name, 'phone_number': phone_number}
                creates.append(dict(table=1, is_global=False, data=to_add))
            elm.end_run(message='Your information has been saved', db_updates=updates, db_creates=creates)
        elif status['func'] == 'check_name':
            name = ask_name()
            data = elm.db_read(1, ['name', 'eq', name], limit=3)
            try:
                print(data['phone_number'])
            except:
                print("No records")
            elm.end_run(message='Name checked')
        else:
            elm.end_run()


def ask_name():
    name = input("Please input name: ")
    return name


def ask_data():
    name = ask_name()
    phone_number = input("Please input phone number: ")
    return name, phone_number


if __name__ == '__main__':
    run_app()
