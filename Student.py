from User import User
from Course import Course
import csv
import os
import pandas as pd
import ast


class Student(User):
    def __init__(self, username, password, stu_num, field, course=None, total_unit=0, total_unit_term=0, term=0):
        """
        :param username: username of student
        :param password: password of student
        :param stu_num: number of student
        :param field: field student
        :param course: list of get courses student
        :param total_unit: total unit
        :param total_unit_term: total unit term
        :param term: term student
        """
        super().__init__(username, password)
        self.stu_num = stu_num
        self.field = field
        self.course = course
        self.total_unit = total_unit
        self.total_unit_term = total_unit_term
        self.term = term

    def show_slc_course(self):
        """
        show selective courses student
        :return:list id courses that student select
        """
        list_id_crs = []
        with open('file_select_course.csv', 'r') as csv_file:
            fieldnames = ['username_student', 'term', 'id_crs', 'name', 'unit', 'name_prof', 'time_exam',
                          'time_class', 'field_crs']
            csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'{", ".join(row)}')
                    line_count += 1
                else:
                    if row['username_student'] == self.username and int(row['term']) == self.term:
                        if row['id_crs'].isdigit():
                            list_id_crs.append(int(row['id_crs']))
                        print(
                            f'\t{row["username_student"]},{row["term"]},{row["id_crs"]},{row["name"]},{row["unit"]},{row["name_prof"]},{row["time_exam"]},{row["time_class"]},{row["field_crs"]}')
        return list_id_crs

    def show_field_course(self):
        """
        show courses student
        """
        with open('file_course.csv', 'r') as csv_file:
            fieldnames = ['id_crs', 'name', 'unit', 'capacity', 'name_prof', 'time_exam', 'time_class', 'field_crs',
                          'status_capacity']
            csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'{", ".join(row)}')
                    line_count += 1
                else:
                    if row['field_crs'] == self.field or row['field_crs'] == 'public':
                        print(
                            f'\t{row["id_crs"]}, {row["name"]}, {row["unit"]}, {row["capacity"]}, {row["name_prof"]}, {row["time_exam"]}, {row["time_class"]}, {row["field_crs"]}')

    def get_course(self, list_id_crs):
        """
        :param list_id_crs:
        :return:
        """
        sum_unit = 0
        list_obj_crs = []

        # check id course input and create instance course
        for id_course in list_id_crs:
            check = Course.search_file_crs('id_crs', id_course)
            if check is False:
                print(f'{id_course} course is not list course')
            else:
                list_obj_crs.append(check)
        # get selective courses
        if type(self.course) is list:
            return 'You are not allowed to select the unit again '
        else:
            if self.course != '':
                self.course = ast.literal_eval(self.course)
            for obj_crs in list_obj_crs:
                for pass_crs in self.course:
                    if pass_crs == obj_crs.id_crs:
                        return f'invalid course because already passed this "{obj_crs.name}" course  '
                if obj_crs.capacity > obj_crs.status_capacity:
                    sum_unit += obj_crs.unit
                else:
                    return f'capacity course {obj_crs.id_crs} full'
            if 20 >= sum_unit >= 10:
                self.total_unit = sum_unit + int(self.total_unit)
                self.total_unit_term = sum_unit
                self.term = 1 + int(self.term)
                for obj_crs in list_obj_crs:
                    obj_crs.status_capacity += 1
                    if self.course == '':
                        self.course = []
                    self.course.append(obj_crs.id_crs)
                    obj_crs.file_selective_crs(self.username, self.term)
                    obj_crs.update_file_course()
                return True
            else:
                return 'Number of units is not allowed :('

    def remove_crs(self, list_id_crs, num_unit_remove):
        """
        :param list_id_crs:
        :param num_unit_remove:
        :return:
        """
        sum_unit = 0
        list_obj_crs = []
        # check id course input and create instance course
        for id_course in list_id_crs:
            check_id = Course.search_file_slc_crs('id_crs', id_course, self.term)
            if check_id:
                check = Course.search_file_crs('id_crs', id_course)
                if check is False:
                    pass
                else:
                    list_obj_crs.append(check)
            else:
                print(f'course {id_course} is not in list selective course ')
        # remove courses
        if type(self.course) is not list:
            self.course = ast.literal_eval(self.course)
        list_course = self.course.copy()
        for obj_crs in list_obj_crs:
            if num_unit_remove >= sum_unit:
                for get_crs in list_course:
                    if get_crs == obj_crs.id_crs:
                        sum_unit += obj_crs.unit
                        self.course.remove(obj_crs.id_crs)
                        obj_crs.status_capacity -= 1
                        obj_crs.update_file_course()
                        obj_crs.update_file_slc_course()
        if sum_unit > 0:
            self.total_unit -= sum_unit
            self.total_unit_term -= sum_unit
            return True
        else:
            return 'Number of units is not allowed :('

    def update_file_stu(self):
        """
        :return:
        """
        df = pd.read_csv("file_student.csv")
        with open('file_student.csv', 'r') as edit_file:
            fieldnames = ['username', 'password', 'stu_num', 'field', 'course', 'total_unit',
                          'total_unit_term', 'term']
            file_stu_r = csv.DictReader(edit_file, fieldnames=fieldnames)
            line = 0
            for row in file_stu_r:
                if self.username == row['username']:
                    df['course'] = df['course'].astype('object')
                    df.at[line - 1, 'course'] = self.course
                    df.loc[line - 1, 'total_unit'] = self.total_unit
                    df.loc[line - 1, 'total_unit_term'] = self.total_unit_term
                    df.loc[line - 1, 'term'] = self.term
                    df.to_csv("file_student.csv", index=False)
                    # return 'selection unit successful :))'
                    return True
                line += 1
            return 'not find username student'

    @classmethod
    def search_file(cls, metric, value_metric):
        """
        :param metric:
        :param value_metric:
        :return:
        """
        check_file = os.path.exists('file_Student.csv')
        if check_file:
            with open('file_Student.csv', 'r') as write_course_csv:
                csv_read = csv.DictReader(write_course_csv)
                for row in csv_read:
                    if row[metric] == value_metric:
                        row = [int(i.strip()) if i.isdigit() else i for i in row.values()]
                        return cls(*row)
        else:
            return False

    @staticmethod
    def show_list_stu():
        """
        print list students
        """
        with open('file_student.csv', 'r') as file_stu:
            fieldnames = ['username', 'password', 'stu_num', 'field', 'course', 'total_unit',
                          'total_unit_term', 'term']
            file_stu_r = csv.DictReader(file_stu, fieldnames=fieldnames)
            line_count = 0
            for row in file_stu_r:
                if line_count == 0:
                    print(f'{", ".join(row)}')
                    line_count += 1
                else:
                    print(
                        f'\t{row["username"]},{row["password"]},{row["stu_num"]},{row["field"]},{row["course"]},{row["total_unit"]},{row["total_unit_term"]},{row["term"]}')

    def file_student(self):
        """
        :return:
        """
        check_file = os.path.exists('file_student.csv')
        if check_file:
            with open('file_student.csv', 'a', newline='') as write_student_csv:
                fieldnames = ['username', 'password', 'stu_num', 'field', 'course', 'total_unit',
                              'total_unit_term', 'term']
                csv_writer = csv.DictWriter(write_student_csv, fieldnames=fieldnames)
                csv_writer.writerow({'username': self.username,
                                     'password': self.password,
                                     'stu_num': self.stu_num,
                                     'field': self.field,
                                     'course': self.course,
                                     'total_unit': self.total_unit,
                                     'total_unit_term': self.total_unit_term,
                                     'term': self.term})

        else:
            with open('file_student.csv', 'a', newline='') as write_student_csv:
                fieldnames = ['username', 'password', 'stu_num', 'field', 'course', 'total_unit',
                              'total_unit_term', 'term']
                csv_writer = csv.DictWriter(write_student_csv, fieldnames=fieldnames)
                csv_writer.writeheader()
                csv_writer.writerow({'username': self.username,
                                     'password': self.password,
                                     'stu_num': self.stu_num,
                                     'field': self.field,
                                     'course': self.course,
                                     'total_unit': self.total_unit,
                                     'total_unit_term': self.total_unit_term,
                                     'term': self.term})
