import hashlib
import csv


class User:
    def __init__(self, username, password):
        """
        :param username: username of user
        :param password: password of user
        """
        self.username = username
        self.password = password

    @staticmethod
    def login(new_username, new_password):
        """
        :param new_username: username student or education
        :param new_password: password student or education
        :return: all attributes student or education in file for create instance. if person is student return 2 and if education return 1
        """
        hash_pass = hashlib.md5(new_password.encode()).hexdigest()
        try:
            with open('file_education.csv', 'r') as file_edu:
                csv_reader = csv.reader(file_edu)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                        pass
                    else:
                        if row[0] == new_username and row[1] == hash_pass:
                            print(f"successful login")
                            row = [int(i.strip()) if i.isdigit() else i for i in row]
                            return 1, row  # login education
            with open('file_student.csv', 'r') as file_stu:
                csv_reader = csv.reader(file_stu)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        if row[0] == new_username and row[1] == hash_pass:
                            row = [int(i.strip()) if i.isdigit() else i for i in row]
                            print(f"successful login")
                            return 2, row  # login student

            print("Your username and/or password do not match ")  # not login
            return 0, 0
        except FileNotFoundError:
            print("Your username and/or password do not match ")  # not login
            return 0, 0

    @staticmethod
    def register(new_username, new_password, name_file):
        """
        :param new_username: username student or education
        :param new_password: password student or education
        :param name_file: name file student or education
        :return: if username is not available return 0 else 1
        """
        hash_pass = hashlib.md5(new_password.encode()).hexdigest()
        try:
            with open('file_education.csv', 'r') as file_edu:
                csv_reader = csv.reader(file_edu)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        if row[0] == new_username:
                            print(f"The username {new_username} is not available")
                            print(f'{50 * "-"}')
                            return 0  # no register
            with open('file_student.csv', 'r') as file_stu:
                csv_reader = csv.reader(file_stu)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        if row[0] == new_username:
                            print(f"The username {new_username} is not available")
                            print(f'{50 * "-"}')
                            return 0  # no register
        except FileNotFoundError:
            if name_file == 'file_student.csv':
                with open('file_student.csv', 'a', newline='') as write_student_csv:
                    fieldnames = ['username', 'password', 'stu_num', 'field', 'course', 'total_unit',
                                  'total_unit_term', 'term']
                    csv_writer = csv.DictWriter(write_student_csv, fieldnames=fieldnames)
                    csv_writer.writeheader()
                    return 1
            elif name_file == 'file_education.csv':
                with open(name_file, 'a', newline='') as edit_file:
                    csv_writer = csv.writer(edit_file)
                    csv_writer.writerow(['username', 'password'])
                    csv_writer.writerow([new_username, hash_pass])
                    print(f"successful register")
                    print(f'{50 * "-"}')
                    return 1
        else:
            if name_file == 'file_education.csv':
                with open(name_file, 'a', newline='') as edit_file:
                    csv_writer = csv.writer(edit_file)
                    csv_writer.writerow([new_username, hash_pass])
                    print(f"successful register")
                    print(f'{50 * "-"}')
                    return 1
