# VOPA
 API Endpoints
  Assigning a lesson to a student (Teacher)

      HTTP Method: `POST`
      URL Path: `/api/assignments`
      Description: Creates a new assignment record. This endpoint is used by teachers to assign a specific lesson to a student.

Viewing assigned, incomplete lessons (Student)

      HTTP Method:`GET`
      URL Path:`/api/assignments?studentId={studentId}&status=incomplete`
      Description:Retrieves a list of lessons that have been assigned to a particular student and have not yet been marked as completed. The query parameters filter the results.

Marking an assigned lesson as complete (Student)**

      HTTP Method: `PUT` or `PATCH`
      URL Path: `/api/assignments/{assignmentId}/complete`
      Description: Updates the status of a specific assignment to 'completed'. `PUT` is used here because it updates the entire resource state to 'complete', while `PATCH` would be used for partial modification. Both are acceptable.

Viewing completion status of assignments (Teacher)**

      HTTP Method: `GET`
      URL Path:`/api/assignments?teacherId={teacherId}`
      Description: Retrieves a list of all assignments made by a specific teacher, including their current status (e.g., incomplete, completed). This allows the teacher to track progress.

 Endpoint Details

POST /api/assignments

This endpoint is used by teachers to create a new assignment.

Request Body

The request body for this endpoint should contain the essential information needed to create an assignment: the ID of the student, the ID of the lesson, and the ID of the teacher who is making the assignment.

json format
{
  "studentId": "stu_12345",
  "lessonId": "les_67890",
  "teacherId": "tch_54321"
}


  * `studentId`: The unique identifier for the student.
  * `lessonId`: The unique identifier for the lesson being assigned.
  * `teacherId`: The unique identifier for the teacher creating the assignment.

Successful Response Body

Upon successful creation of the assignment, the API should return the details of the newly created assignment, including its unique ID and a default status (e.g., 'incomplete'). This allows the client to confirm the assignment's creation and reference it later.

json format
{
  "assignmentId": "asg_98765",
  "studentId": "stu_12345",
  "lessonId": "les_67890",
  "teacherId": "tch_54321",
  "status": "incomplete",
  "createdAt": "2025-08-20T22:30:00Z"
}

    `assignmentId`: The unique ID assigned to the new assignment.
    `status`: The current status of the assignment, which is initially `incomplete`.
    `createdAt`: A timestamp indicating when the assignment was created.
System consideration
1. Permissions and Authorization
This is the most critical part. You need to be absolutely sure that only a teacher can assign a lesson and that a student can only mark their own lessons as complete.

Teacher Actions: The system must verify that the user making the POST /api/assignments request has a "teacher" role. It should also check that a teacher can't assign a lesson to a student who isn't in their class, preventing them from assigning work to random students in the school.

Student Actions: When a student uses the PUT /api/assignments/{assignmentId}/complete endpoint, the system has to confirm that the studentId associated with that assignment matches the ID of the student making the request. This prevents a student from completing another student's work.

2. Database Schema Impact
Introducing a new feature like this means the database needs a new way to store the data. The most straightforward approach is to create a new table, perhaps called assignments.

This table would need to link a student, a teacher, and a lesson together. The bare minimum columns would be:

assignment_id (Primary Key)

student_id (Foreign Key)

lesson_id (Foreign Key)

teacher_id (Foreign Key)

status (e.g., 'incomplete', 'completed')

created_at

completed_at (to track when a lesson was finished)

Creating this separate table keeps your existing students, teachers, and lessons tables clean and avoids cluttering them with assignment-specific information. It's a clean and scalable way to manage the new relationship between these existing entities.
