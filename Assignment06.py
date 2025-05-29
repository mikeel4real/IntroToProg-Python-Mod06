# ------------------------------------------------------------------------------------------ #
# Title: Assignment06_Starter
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#  Michael Keel,mkeel, 05/28/2025, Created Script
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
# Define the Data Constants
# FILE_NAME: str = "Enrollments.csv"
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables and constants
student_first_name: str = ''  # Holds the first name of a student entered by the user.
student_last_name: str = ''  # Holds the last name of a student entered by the user.
course_name: str = ''  # Holds the name of a course entered by the user.
student_data: dict = {}  # one row of student data
students: list = []  # a table of student data
file = None  # Holds a reference to an opened file.
menu_choice: str = ''  # Hold the choice made by the user.


# Processor goes here
class FileProcessor:
    """Process functions to be used with json
    Change Log:
    Michael Keel, 05/23/2025, Created
    Michael Keel, 05/27/2025, Added R/W function

    :param file_name: string data with name of file to read
    :param student_data:list of dictionary rows filled with file data
    """
    @staticmethod

    def read_data_from_file(file_name:str, student_data: list):
        '''Function attempts open/read of .json. The contents are then
        streamed into a list. Error handling supported for invalid file format
        and missing file
        Change Log:
        Michael Keel, 05/27/25, Completed function creation
        :return: saved data in list
        '''

        file=None
        #local var

        try:
            file=open(file_name,'r')
            student_data = json.load(file)
        except FileNotFoundError as e:
            IO.output_error_messages('Text file not found', e)
        except Exception as e:
            IO.output_error_messages('Unknown exception', e)
        finally:
            if not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """Function outputs the course registration data into a to a JSON file
        Change Log:
        Michael Keel, 05/27/25, created
        :return: None
        """

        try:
            file = open(file_name, 'w')
            json.dump(student_data, file, indent=2)
            file.close()
            print('The following data was written to file:')
            for student in student_data:
                print(f"Student {student["FirstName"]} "
                      f"{student["LastName"]} is enrolled in {student["CourseName"]}")
        except TypeError as e:
            IO.output_error_messages(
                "Ensure data is in JSON format", e)
        except Exception as e:
            IO.output_error_messages(
                "Unspecified error. Try again.", e)
        finally:
            if file and not file.closed:
                #added above syntax based off of office hours
                #makes it so that files not written do not give this error
                file.close()

#Presentation
class IO:
    #used from SepOfConcern video @4:50-8:15
    """Functions used to input data from user and output to relevant tasks
    Change Log:
    Michael Keel, 05/27/2025, Created Function
    """
    @staticmethod
    def output_error_messages(message:str, error: Exception=None):
        """Custom errors to the user
        Change Log:
        Michael Keel, 05/27/2025
        """
        print(message, '\n')
        if error is not None:
            print(error, error.__doc__, type(error), sep='\n')
    @staticmethod
    def output_menu(menu: str):
        """Display menu to user, Michael Keel, created 05/27/2025"""
        print(menu)
    @staticmethod
    def input_menu_choice():
        """Store user input selection from menu, Michael Keel, 05/27/2025"""
        choice=''
        try:
            choice=input('Enter menu option from 1-4: ')
            if choice not in ('1','2','3','4'):
                raise Exception('Must enter a valid number entry')
        except Exception as e:
            IO.output_error_messages(e.__str__())
        return choice

    @staticmethod
    def input_student_data(student_data: list):
        """Stores student data as a table, provides some error handling.
        Change Log: Michael Keel, 05/27/2025
        """
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Please enter the name of the course: ")
            student = {"FirstName": student_first_name,
                            "LastName": student_last_name,
                            "CourseName": course_name}
            students.append(student)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(
                'The values you have entered are the incorrect type', e)
        except Exception as e:
            IO.output_error_messages('Unspecified error', e)
        return student_data

    @staticmethod
    def output_student_courses(student_data: list):
        """Function lists entries received, Michael Keel, 05/27/2025"""
        print('The current data is')
        for student in student_data:
            print(f'Student {student["FirstName"]} '
                  f'{student["LastName"]} is enrolled in {student["CourseName"]}')
            print('='*50)



###Below starts main body of program

students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

while True:
    IO.output_menu(menu=MENU)
    menu_choice=IO.input_menu_choice()

    ##Import user data
    if menu_choice =='1':
        IO.input_student_data(student_data=students)
        continue

    #Present current
    elif menu_choice =='2':
        IO.output_student_courses(student_data=students)
        continue

    #Save data
    elif menu_choice =='3':
        FileProcessor.write_data_to_file(file_name=FILE_NAME,student_data=students)
        continue

    #Close
    elif menu_choice == '4':
        break

    else:
        print('Please select a valid menu option')
print('Program Closed')