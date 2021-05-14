import logging
from Student import Student
from User import User
from Education import EducationAdmin

my_logger = logging.getLogger(__name__)
my_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('File_log.log')
file_handler.setLevel(logging.INFO)
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(log_format)
my_logger.addHandler(file_handler)


def menu_student(obj_stu):
    while True:
        print(f'{50 * "*"} + Welcome {obj_stu.username} + {50 * "*"}\n'
              f'1- Show field course list\n'
              f'2- Selection unit\n'
              f'3- Result selection unit(Show selective course list and sum unit)\n'
              f'4- Remove course\n'
              f'5- Quit')
        print(f'{50 * "-"}')
        slc_item = input(f'Please select above item --> ')
        print(f'{50 * "-"}')
        try:
            assert slc_item in ['1', '2', '3', '4', '5']
            if slc_item == '1':  # Show field course list
                obj_stu.show_field_course()

            elif slc_item == '2':  # Selection unit
                list_id_crs = input("Enter id selective course :").split(',')
                status_slc_unit = obj_stu.get_course(list_id_crs)
                if status_slc_unit is True:
                    status_update_file = obj_stu.update_file_stu()
                    if status_update_file is True:
                        print('selection unit successful :))')
                        my_logger.info('selection unit successful')
                    else:
                        print(status_update_file)
                else:
                    print(status_slc_unit)

            elif slc_item == '3':  # Result selection unit
                obj_stu.show_slc_course()
                print(f'term:{obj_stu.term}\n'
                      f'total unit:{obj_stu.total_unit}\n'
                      f'total unit term:{obj_stu.total_unit_term}')
            elif slc_item == '4':  # Remove course
                obj_stu.show_slc_course()
                list_id_crs = input("Enter id course for remove:").split(',')
                status_rm_crs = obj_stu.remove_crs(list_id_crs, 6)
                if status_rm_crs is True:
                    status_update_file = obj_stu.update_file_stu()
                    if status_update_file is True:
                        print('remove course successful :))')
                        my_logger.info('remove course successful')
                    else:
                        print(status_update_file)
                else:
                    print(status_rm_crs)
            elif slc_item == '5':
                break
        except:
            my_logger.error('mistake item', exc_info=True)
            print('Please enter item correct')


def menu_education(obj_edu):
    while True:
        print(f'{50 * "*"} + Welcome {obj_edu.username} + {50 * "*"}\n'
              f'1- Enter information course\n'
              f'2- Enter information and register student\n'
              f'3- reject and accept selective unit student\n'
              f'4- Quit')
        print(f'{50 * "-"}')
        slc_item = input(f'Please select above item --> ')
        print(f'{50 * "-"}')
        try:
            assert slc_item in ['1', '2', '3', '4']
            if slc_item == '1':  # Enter information course
                # 10,network,3,20,ali,20/4/1400,8 to 10,computer
                course = input(
                    'Enter id_crs, name, unit, capacity, name_prof, time_exam, time_class, field_crs :').split(
                    ',')
                status_crs = obj_edu.create_course(course)  # enter information course
                if status_crs == 0:
                    print('id course is invalid')
                else:
                    my_logger.info('course added', exc_info=True)
                    print('Course added successfully')

            elif slc_item == '2':  # register student and create object student
                student = input('Enter username, password, stu_num, field:').split(',')
                status_stu = obj_edu.register_stu(student)
                if status_stu == 0:
                    print('student already register')
                else:
                    obj_stu = Student(*status_stu)
                    obj_stu.file_student()
                    print('student register successfully')

            elif slc_item == '3':  # reject and accept selective unit student
                Student.show_list_stu()
                username_stu = input("Enter username a student in above list --> ")
                check_user = Student.search_file('username', username_stu)
                if check_user is False:
                    return 'username student invalid!!! please enter username correct :('
                else:
                    list_id_crs = check_user.show_slc_course()
                    item = input('reject or accept selective unit student:\n'
                                 '1- accept\n'
                                 '2- reject\n'
                                 'Please select above item -->')
                    if item == '1':
                        print(f'accept selection unit {check_user.username}')
                        my_logger.info('accept selective unit')
                    elif item == '2':
                        status_rm_crs = check_user.remove_crs(list_id_crs, 20)
                        if status_rm_crs is True:
                            status_update_file = check_user.update_file_stu()
                            if status_update_file is True:
                                print('remove course successful :))')
                            else:
                                print(status_update_file)
                        else:
                            print(status_rm_crs)
            elif slc_item == '4':
                break
        except:
            print('Please enter item correct')
            my_logger.error('mistake item', exc_info=True)


def menu_login():
    cnt = 1
    list_username = []
    while True:
        print('Menu Login :)')
        new_username = input('Enter username --> ')
        new_password = input('Enter password --> ')
        list_username.append(new_username)
        sts_login = User.login(new_username, new_password)
        if sts_login[0] == 2:  # login students
            stu = Student(*sts_login[1])
            my_logger.info('login student')
            menu_student(stu)
        elif sts_login[0] == 1:  # login education
            edu = EducationAdmin(*sts_login[1])
            my_logger.info('login education')
            menu_education(edu)
        elif sts_login[0] == 0:
            set_user = set(list_username)
            if len(set_user) == 1:
                cnt += 1
                my_logger.info('Failed login')
            if cnt > 3:
                print('Three failed logins :( ')
                break


def menu():
    while True:
        print(f'{50 * "*"} + University + {50 * "*"}\n'
              f'1- Register education\n'
              f'2- Login\n'
              f'3- Quit')
        print(f'{50 * "-"}')
        slc_item = input(f'Please select above item --> ')
        print(f'{50 * "-"}')
        try:
            assert slc_item in ['1', '2', '3']
            if slc_item == '1':
                while True:
                    print('Menu Register')
                    new_username = input('Enter username --> ')
                    new_password = input('Enter password --> ')
                    sts_reg = EducationAdmin.register(new_username, new_password, 'file_education.csv')
                    if sts_reg == 0:
                        pass
                    else:
                        menu_login()
                        break
            elif slc_item == '2':
                menu_login()
            elif slc_item == '3':
                break
        except:
            print('Please Enter correct item !!!')
            my_logger.error('mistake item', exc_info=True)


menu()
