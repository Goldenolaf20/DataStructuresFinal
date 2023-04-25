# Name : HomeworkTracker.py
# Author: Zoey Klehm
# Created : 4/24/2023
# Course: CIS 152 - Data Structure
# Version: 1.0
# OS: Windows 11
# IDE: PyCharm 3.10
# Copyright : This is my own original work based on specifications issued by our instructor
# Description : An app that creates a GUI to allow users to track homework assignments for various courses, having
# functionality to create assignments, complete assignments, query next assignment from specified course, and query all
# assignments from selected course
#            Input: Assignments for courses
#            Output: Either the next assignments due, or all assignments due, for the specified course
# Academic Honesty: I attest that this is my original work.
# I have not used unauthorized source code, either modified or unmodified.
# I have not given other fellow student(s) access to my program.


from datetime import date
from HomeworkTracker import Assignment
from HomeworkTracker import HomeworkTracker
import tkinter as tk
from tkcalendar import DateEntry


def create_assignment(homework_tracker):  # takes the necessary fields from the tkinter GUI(time to complete, due date,
    # assignment desc, and course id), and runs the method to add the assignment to the class, or add the class to the
    # list of classes
    homework_tracker.add_assignments_list(courseInput.get(1.0, "end-1c"),
                                          Assignment(int(timeToCompleteInput.get(1.0, "end-1c")),
                                                     dueDateInput.get_date(),
                                                     assignDescInput.get(1.0, "end-1c"),
                                                     courseInput.get(1.0, "end-1c")))

    addAssignmentLabel.config(text="New assignment successfully added to course: " + courseInput.get(1.0, "end-1c"))

    update_available_courses(homework_tracker)
    collect_assignments(homework_tracker)


def update_available_courses(homework_tracker):  # updates the GUI element that shows all courses that are in the
    # homework tracker
    displayStr = ""

    for course in homework_tracker.courses.keys():
        displayStr += course + ", "

    availableCoursesDisplay.config(text=displayStr[:-2])


def display_next_assignment(homework_tracker):  # runs method from homeworkTracker class that displays the next due
    # assignment from the course that the user specified
    outputDisplayNextAssignment.config(text="Next assignment for " + courseInput.get(1.0, "end-1c") + ":\n" +
                                            homework_tracker.find_next_assignment(courseInput.get(1.0, "end-1c")))


def display_all_assignments(homework_tracker):  # runs method from homeworkTracker class that displays all assignments
    # from the specified course
    outputDisplayAllAssignments.config(text="All Assignments for " + courseInput.get(1.0, "end-1c") + ":\n" +
                                            homework_tracker.display_course_assignments(courseInput.get(1.0, "end-1c")))


def collect_assignments(homework_tracker):  # creates a list of all the assignments in the homework tracker, then adds
    # the assignments to the OptionMenu in the tkinter to allow the user to select assignments to complete, as well as
    # allowing for the OptionMenu to update as the user adds new assignments
    list_of_assignments = []
    for key in homework_tracker.courses.keys():
        assignment_count = 1
        for assignment in homework_tracker.courses.get(key):
            list_of_assignments.append("Assignment " + str(assignment_count) + " of Course " + str(key)
                                       + ": " + assignment.desc)
            assignment_count += 1

    menu = assignmentToCompleteMenu["menu"]
    menu.delete(0, "end")

    for assignment in list_of_assignments:
        menu.add_command(label=assignment, command=lambda value=assignment: selected_option.set(value))


def complete_assignment(homework_tracker):  # completes the assignment currently selected in the OptionMenu
    selectedOption = selected_option.get()

    if selectedOption != "Select an Assignment":  # checks the user actually selected an assignment
        splitQuery = selectedOption.split(": ")
        selectedCourse = splitQuery[0].split("Course ")
        selectedCourse = selectedCourse[-1]  # selects the text after the word Course and before the :
        selectedAssignment = splitQuery[1]  # selects the description of the assignment/everything after the :

        list_of_assignments = homework_tracker.courses.get(selectedCourse)

        for assignment in list_of_assignments:
            if assignment.desc == selectedAssignment:  # if the descriptions match
                assignment.completed = not assignment.completed  # set the assignment completed bool to the opposite val

                assignmentUpdatedDisplay.config(text="Assignment: " + selectedOption + " successfully set to: "
                                                     + str(assignment.completed))
    else:
        assignmentUpdatedDisplay.config(text="Error, no assignment was selected")


if __name__ == "__main__":
    testHomeworkTracker = HomeworkTracker()  # default homework tracker

    dataStructuresFinal = Assignment(40, date(2023, 5, 4), "A culmination of the work we have done "
                                                           "throughout the semester", "CIS152")
    testAssignment1 = Assignment(10, date(2023, 4, 23), "test assignment 1 for data structures", "CIS152")
    testAssignment2 = Assignment(10, date(2023, 5, 1), "test assignment 2 for data structures", "CIS152")

    testAssignment1_class2 = Assignment(5, date(2023, 5, 4), "test assignment 1 class 2", "ABC123")
    testAssignment2_class2 = Assignment(10, date(2023, 5, 4), "test assignment 2 class 2", "ABC123")
    testAssignment3_class2 = Assignment(5, date(2023, 5, 4), "test assignment 3 class 2", "ABC123")

    testAssignment_class3 = Assignment(10, date(2023, 4, 23), "test assignment class 3", "DEF456")

    testHomeworkTracker.add_assignments_list(testAssignment1.courseId, testAssignment1)
    testHomeworkTracker.add_assignments_list(testAssignment2.courseId, testAssignment2)
    testHomeworkTracker.add_assignments_list(dataStructuresFinal.courseId, dataStructuresFinal)

    testHomeworkTracker.add_assignments_list(testAssignment1_class2.courseId, testAssignment1_class2)
    testHomeworkTracker.add_assignments_list(testAssignment2_class2.courseId, testAssignment2_class2)
    testHomeworkTracker.add_assignments_list(testAssignment3_class2.courseId, testAssignment3_class2)

    testHomeworkTracker.add_assignments_list(testAssignment_class3.courseId, testAssignment_class3)

    # above is code for creating the preset data for the project, below is the code to create the GUI to accept user
    # commands and data, as well as display the data provided above

    GUI = tk.Tk()
    GUI.geometry("1200x600")
    GUI.title("Homework Tracker")

    courseLabel = tk.Label(GUI, text="Course(used for both adding, and querying assignments):")
    courseInput = tk.Text(GUI, height=1)
    timeToCompleteLabel = tk.Label(GUI, text="Time assignment will take to complete:")
    timeToCompleteInput = tk.Text(GUI, height=1)
    dueDateLabel = tk.Label(GUI, text="Enter due date:")
    dueDateInput = DateEntry(GUI, height=1)
    assignDescLabel = tk.Label(GUI, text="Enter assignment description:")
    assignDescInput = tk.Text(GUI, height=3)
    addAssignmentButton = tk.Button(GUI, text="Add Assignment", command=lambda: create_assignment(testHomeworkTracker))
    addAssignmentLabel = tk.Label(GUI, text="")

    courseLabel.grid(row=1, column=0)
    courseInput.grid(row=1, column=1)
    timeToCompleteLabel.grid(row=2, column=0)
    timeToCompleteInput.grid(row=2, column=1)
    dueDateLabel.grid(row=3, column=0)
    dueDateInput.grid(row=3, column=1)
    assignDescLabel.grid(row=4, column=0)
    assignDescInput.grid(row=4, column=1)
    addAssignmentButton.grid(row=5, column=0)
    addAssignmentLabel.grid(row=6, column=0, pady=10)

    # above is all the code responsible for the tkinter GUI creating new assignments, below will be the code to
    # display the assignments for each course

    availableCoursesLabel = tk.Label(GUI, text="Available courses:")
    availableCoursesDisplay = tk.Label(GUI, text="")
    outputDisplayNextAssignment = tk.Label(GUI, text="")
    outputDisplayAllAssignments = tk.Label(GUI, text="")
    displayNextAssignmentButton = tk.Button(GUI, text="Display Next Assignment From Selected Course",
                                            command=lambda: display_next_assignment(testHomeworkTracker))
    displayAllAssignmentsFromCourseButton = tk.Button(GUI, text="Display All Assignments From Selected Course",
                                                      command=lambda: display_all_assignments(testHomeworkTracker))

    update_available_courses(testHomeworkTracker)

    availableCoursesLabel.grid(row=8, column=0)
    availableCoursesDisplay.grid(row=8, column=1)
    outputDisplayNextAssignment.grid(row=9, column=0)
    outputDisplayAllAssignments.grid(row=9, column=1)
    displayNextAssignmentButton.grid(row=10, column=0)
    displayAllAssignmentsFromCourseButton.grid(row=10, column=1)

    # completing an assignment is getting its own spot, bc it is a different process compared to the rest of the GUI

    assignmentToCompleteLabel = tk.Label(GUI, text="Select assignment to complete:")
    assignmentToCompleteButton = tk.Button(GUI, text="Toggle Complete on Selected Assignment",
                                           command=lambda: complete_assignment(testHomeworkTracker))
    assignmentUpdatedDisplay = tk.Label(GUI, text="")

    assignmentsList = ["filler"]

    selected_option = tk.StringVar(GUI)

    selected_option.set("Select an Assignment")

    assignmentToCompleteMenu = tk.OptionMenu(GUI, selected_option, *assignmentsList)

    collect_assignments(testHomeworkTracker)

    assignmentToCompleteLabel.grid(row=11, column=0)
    assignmentToCompleteMenu.grid(row=11, column=1)
    assignmentToCompleteButton.grid(row=12, column=0)
    assignmentUpdatedDisplay.grid(row=13, column=0)

    # and finally, a button to exit the tkinter GUI

    exitButton = tk.Button(GUI, text="Exit", command=GUI.destroy)
    exitButton.grid(row=100, column=0)

    GUI.mainloop()  # runs the GUI
