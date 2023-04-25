from datetime import date


def bubble_sort(arr):  # bubble sorts the times the courses will take to complete, from longest to shortest
    n = len(arr)
    swapped = False
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] < arr[j + 1]:
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

        if not swapped:
            return


class Assignment:  # contains the individual assignments of a course
    def __init__(self, time_to_complete, due_date, desc, course_id):
        self.timeToComplete = time_to_complete  # tracks how long user estimates assignment will take them, in hours
        self.dueDate = due_date  # tracks when the assignment is due
        self.desc = desc  # a short description of what the assignment is
        self.courseId = course_id  # tracks which course the assignment is for
        self.nextAssignment = None
        self.completed = False

    def queue_next_assignment(self, next_assignment):  # sets the next assignment of the current assignment
        self.nextAssignment = next_assignment

    def days_until_due(self):  # method created to return the amount of days until the assignment is due
        days = (self.dueDate - date.today()).days

        match days:
            case 1:
                return "1 day until due"
            case -1:
                return "1 day late"
            case 0:
                return "Assignment is due today"

        if days < 0:
            return str(days) + " days late"
        elif days > 0:
            return str(days) + " days until due"

    def add_next_assignment(self, next_assignment):
        self.nextAssignment = next_assignment


class HomeworkTracker:  # holds all the courses, is a queue
    def __init__(self):
        self.head = None
        self.tail = None
        self.courses = {}  # is a dictionary and a queue of assignments, ordered by earliest due dates and longest
        # time to finish

    def add_assignments_list(self, course_id, assignment):  # method properly places the new assignment provided
        if course_id not in self.courses:
            self.courses.update({course_id: [assignment]})
        else:
            assignments_list = self.courses.get(course_id)
            if type(assignments_list) is Assignment:
                last_assignment = assignments_list
            else:
                last_assignment = assignments_list[len(assignments_list) - 1]
            last_assignment.add_next_assignment(assignment)

            self.courses.get(course_id).append(assignment)

        prev_assignment = None  # begins the portion that sorts the items in the list to the correct order
        assignments_to_sort = self.courses.get(course_id).copy()
        self.courses.get(course_id).clear()
        while len(assignments_to_sort) != 0:
            earliest_due_dates = []
            earliest_due_date_found = date(9999, 12, 31)
            for assignment in assignments_to_sort:
                if assignment.dueDate < earliest_due_date_found:
                    earliest_due_date_found = assignment.dueDate
                    earliest_due_dates.clear()
                    earliest_due_dates.append(assignment)
                elif assignment.dueDate == earliest_due_date_found:
                    earliest_due_dates.append(assignment)

            for assignment in earliest_due_dates:
                self.courses.get(course_id).append(assignment)

                assignments_to_sort.remove(assignment)

                if prev_assignment is not None:
                    prev_assignment.add_next_assignment(assignment)
                prev_assignment = assignment

        self.courses.get(course_id)[len(self.courses.get(course_id)) - 1].add_next_assignment(None)

        self.arrange_queue()  # after adding a new assignment, sort the queue to verify that order of courses is correct

    def find_next_assignment(self, course_id):  # method finds the next assignment that is not completed for the
        # specified course
        this_course = self.courses.get(course_id)
        assignment_count = 1
        if this_course is not None:
            if type(this_course) == Assignment:
                assignment = this_course
                if assignment.completed is False:
                    return "Assignment " + str(assignment_count) + ": " + assignment.desc + "\nDays until due: " \
                           + assignment.days_until_due()
            else:
                for assignment in this_course:
                    if not assignment.completed:
                        return "Assignment " + str(assignment_count) + ": " + assignment.desc + "\nDays until due: " \
                               + assignment.days_until_due()
                    assignment_count += 1

            return "No Assignment Found"
        else:
            return "Invalid Course"

    def display_course_assignments(self, course_id):  # method displays all assignments for the specified course
        this_course = self.courses.get(course_id)
        assignment_count = 1
        if this_course is not None:
            if type(this_course) == Assignment:
                assignment = this_course
                return "Assignment " + str(assignment_count) + ": " + assignment.desc + "\nDays until due: " \
                       + assignment.days_until_due() + "\nCompleted: " + str(assignment.completed)
            else:
                displayStr = ""
                for assignment in this_course:
                    displayStr += "Assignment " + str(assignment_count) + ": " + assignment.desc + "\nDays until due: "\
                                  + assignment.days_until_due() + "\nCompleted: " + str(assignment.completed) + "\n\n"
                    assignment_count += 1

                return displayStr
        else:
            return "Invalid Course"

    def arrange_queue(self):  # arranges queue based off of course with the earliest due dates, and time to complete, if
        # the assignments are not completed
        newOrder = []

        oldOrderWithDueDateAndTotalTime = []

        queueCopy = self.courses.copy()

        validAssignmentFound = False

        courseTimesToComplete = {}
        for courseKey in queueCopy.keys():
            firstAssignment = None
            for assignment in queueCopy.get(courseKey):
                if firstAssignment is None and not assignment.completed:
                    firstAssignment = assignment
                    validAssignmentFound = True
                if courseKey in courseTimesToComplete.keys() and not assignment.completed:
                    courseTimesToComplete.update({courseKey: courseTimesToComplete.get(courseKey)
                                                             + assignment.timeToComplete})
                elif courseKey not in courseTimesToComplete.keys() and not assignment.completed:
                    courseTimesToComplete.update({courseKey: assignment.timeToComplete})

            oldOrderWithDueDateAndTotalTime.append(
                [courseKey, firstAssignment.dueDate, courseTimesToComplete.get(courseKey)])

        if not validAssignmentFound:
            return "No Classes found with uncompleted assignments"

        self.courses.clear()

        while len(oldOrderWithDueDateAndTotalTime) != 0:
            earliest_due_date = date(9999, 12, 31)
            earliest_due_courses = []
            for course in oldOrderWithDueDateAndTotalTime:
                if course[1] < earliest_due_date:
                    earliest_due_date = course[1]
                    earliest_due_courses.clear()
                    earliest_due_courses.append(course)
                elif course[1] == earliest_due_date:
                    earliest_due_courses.append(course)

            if len(earliest_due_courses) != 1:
                times_to_complete = []
                for course in earliest_due_courses:
                    times_to_complete.append(course[2])

                bubble_sort(times_to_complete)
                courses_to_sort = earliest_due_courses.copy()
                earliest_due_courses.clear()

                while len(courses_to_sort) != 0:
                    for course in courses_to_sort:
                        if course[2] == times_to_complete[0]:
                            earliest_due_courses.append(course)
                            times_to_complete.remove(times_to_complete[0])
                            courses_to_sort.remove(course)

            for course in earliest_due_courses:
                newOrder.append(course[0])
                oldOrderWithDueDateAndTotalTime.remove(course)

        while len(newOrder) != 0:
            self.courses.update({newOrder[0]: queueCopy.get(newOrder[0])})
            newOrder.remove(newOrder[0])

    # def display_course_order(self):  # deprecated method for showing the list of all courses currently created
    #     return list(self.courses.keys())
