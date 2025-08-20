from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import uuid

app = Flask(__name__)
CORS(app)

users_db = {
    'user-1': {'name': 'You (Teacher)', 'role': 'teacher'},
    's_101': {'name': 'Alice (Student)', 'role': 'student'},
    's_102': {'name': 'Bob (Student)', 'role': 'student'},
    's_103': {'name': 'Charlie (Student)', 'role': 'student'},
}

lessons_db = {
    'l_1': {'name': 'Algebra Fundamentals'},
    'l_2': {'name': 'Introduction to Biology'},
    'l_3': {'name': 'World History'},
}

def init_db():
    conn = sqlite3.connect('vschool.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            assignment_id TEXT PRIMARY KEY,
            teacher_id TEXT NOT NULL,
            student_id TEXT NOT NULL,
            lesson_id TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/assignments', methods=['POST'])
# POST: Assigns a new lesson to a specific student from list 
def assign_lesson():
    data = request.json
    teacher_id = data.get('teacherId')
    student_id = data.get('studentId')
    lesson_id = data.get('lessonId')

    if not teacher_id or not student_id or not lesson_id:
        return jsonify({'error': 'Missing required fields'}), 400

    new_assignment_id = str(uuid.uuid4())
    status = 'incomplete'
    
    conn = sqlite3.connect('vschool.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO assignments VALUES (?, ?, ?, ?, ?)
    ''', (new_assignment_id, teacher_id, student_id, lesson_id, status))
    conn.commit()
    conn.close()

    return jsonify({
        'message': 'Assignment created successfully.',
        'assignment_id': new_assignment_id,
    }), 201

@app.route('/api/assignments/<assignment_id>/complete', methods=['PUT'])
# PUT: Marks a specific assignment as complete or incomplete.
def complete_assignment(assignment_id):
    conn = sqlite3.connect('vschool.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE assignments SET status = "completed" WHERE assignment_id = ?', (assignment_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Assignment not found'}), 404

    return jsonify({'message': 'Assignment marked as completed'}), 200

@app.route('/api/assignments/me', methods=['GET'])
# GET: Retrieves all assignments for the current user with status i only use one view for both only for understanding.
def get_my_assignments():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'error': 'userId is required'}), 400

    conn = sqlite3.connect('vschool.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM assignments WHERE teacher_id = ? OR student_id = ?', (user_id, user_id))
    assignments_data = cursor.fetchall()
    conn.close()

    assignments_list = []
    for row in assignments_data:
        assignments_list.append({
            'assignment_id': row[0],
            'teacher_id': row[1],
            'student_id': row[2],
            'lesson_id': row[3],
            'status': row[4],
            'teacher_name': users_db.get(row[1], {}).get('name', 'Unknown'),
            'student_name': users_db.get(row[2], {}).get('name', 'Unknown'),
            'lesson_name': lessons_db.get(row[3], {}).get('name', 'Unknown'),
        })
