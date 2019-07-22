import binascii
import os
from elmsdk import ELMSDK
import sys
import xlwt


def run_app(key, dev_mode=False):
    if dev_mode:
        elm = ELMSDK(key, dev_mode=True)
        elm.setup_dev_run(dev_mode)
    else:
        elm = ELMSDK(key)

    avaliable_functions = ["add", "check_name", "exit", "save"]
    menu = [
        ['check_name', 'Find a number for name'],
        ['add', 'Add_number'],
        ['save', 'Save data'],
        ['exit', 'Exit']
    ]

    while True:
        status = elm.begin_run()
        if status['func'] == "start":
            elm.end_run(message="What would you like to do?", continue_run=dict(func='after_choice',
                                                                                inputs=[dict(name="choice",
                                                                                             options=menu)]))

        if status['func'] == "after_choice":
            if dev_mode:
                next_function = input(
                    "Enter 'add' to add or update data, "
                    "'check_name' to get a number for a name, "
                    "'save' to save it or "
                    "'exit' to close: ")
            else:
                next_function = status["inputs"].get('choice', '')
            if next_function in avaliable_functions:
                status['func'] = next_function
                inputs = get_inputs(next_function)
                if inputs:
                    elm.end_run(message='Please input the following information',
                                continue_run={'func': next_function, 'inputs': inputs})
                else:
                    elm.end_run(message="Click 'Run' to continue",
                                continue_run={'func': next_function})
            else:
                elm.end_run(message='Invalid input', continue_run={'func': "start"})
        elif status['func'] == "exit":
            elm.end_run(message='Thanks for using our tools.')
        elif status['func'] == 'add':
            if dev_mode:
                username, phone_number = ask_data()
            else:
                username = status["inputs"].get('username', '')
                phone_number = status["inputs"].get("phone_number", '')
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
            if dev_mode:
                elm.end_run(message='Your information has been saved', continue_run={'func': "start"},
                            db_updates=updates, db_creates=creates)
            else:
                elm.end_run(message='Your information has been saved', db_updates=updates, db_creates=creates,
                            continue_run={'func': "start"})

        elif status['func'] == 'check_name':
            if dev_mode:
                username = ask_username()
            else:
                username = status["inputs"].get('username', '')
            data = elm.db_read(1, ['username', 'eq', username], limit=3)
            try:
                message = data[0]['phone_number']
            except:
                message = "No records"
            if dev_mode:
                print(message)
                elm.end_run(message=message, continue_run={'func': "start"})
            else:
                elm.end_run(message=message, continue_run={'func': "start"})

        elif status['func'] == 'save':
            # data = elm.db_read(1, ['username', 'eq', username], limit=3)
            data = elm.db_read(1, [])
            workbook = xlwt.Workbook(encoding='ascii')
            worksheet = workbook.add_sheet('My Worksheet')
            for i in range(len(data)):
                elem = data[i]
                worksheet.write(i, 0, elem["username"])
                worksheet.write(i, 1, elem["phone_number"])
            fname = "{0}/{1}.xlsx".format("/tmp", binascii.b2a_hex(os.urandom(17)).decode("utf-8"))
            workbook.save(fname)
            key = elm.file_upload(fname)
            output_link = elm.file_download_link(key, "Data.xlsx")
            message = "Data is saved"

            if dev_mode:
                print(output_link)
                elm.end_run(message=message, continue_run={'func': "start"})
            else:
                elm.end_run(message=message, link=output_link, continue_run={'func': "start"})


def ask_username():
    username = input("Please input name: ")
    return username


def ask_data():
    username = ask_username()
    phone_number = input("Please input phone number: ")
    return username, phone_number


def get_inputs(func):
    if func == "add":
        inputs = get_add_inputs()
    elif func == "check_name":
        inputs = get_check_inputs()
    elif func == "save":
        inputs = []
    else:
        inputs = []
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


if __name__ == '__main__':
    if len(sys.argv) > 2:
        run_app(sys.argv[1], sys.argv[2])
    else:
        run_app(sys.argv[1])
