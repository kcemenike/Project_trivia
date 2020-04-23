import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_server = "localhost:5432"
        self.database_name = "trivia_test"
        self.database_user = "test_user"
        self.database_password = "test_password"
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_server}/{self.database_name}"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = Question(
            question = "new question",
            answer = "new answer",
            category = 1,
            difficulty = 1
        )
        self.new_category = Category("Test")
        
        self.new_question.insert()
        self.new_category.add()

    def tearDown(self):
        """Executed after reach test"""
        self.new_question.delete()
        self.new_category.delete()
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


    def test_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertLessEqual(data['total_questions'], 10) # test that pagination works
        self.assertTrue(len(data['questions']))

    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_category_questions(self):
        res = self.client().get(f'/categories/{self.new_question.category}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(int(data['category']), self.new_question.category)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total'])

    def test_get_category_questions_404(self):
        res = self.client().get(f'/categories/9999/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Sorry, resource unavailable")


    def test_unreachable_page_number(self):
        res = self.client().get('/questions?page=9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Sorry, resource unavailable")

    def test_unreachable_category_number(self):
        res = self.client().get('/categories/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Sorry, resource unavailable")

    def test_delete_question(self):
        # create question to be deleted
        question = Question("new question", "new answer", 1, 1)
        question.insert()
        question_id = question.id
        
        # delete question and get response
        res = self.client().delete(f"questions/{question_id}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check if deleted question no longer exists
        deleted_question = Question.query.get(question_id)
        self.assertEqual(deleted_question, None)

    def test_delete_question_404(self):
        res = self.client().delete("questions/askfueso")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Sorry, resource unavailable")

    def test_add_question(self):
        new_question = {
            'question': 'Who is the first man?',
            'answer': 'Adam',
            'category': 1,
            'difficulty': 1
        }
        oldTotal = len(Question.query.all())
        
        # Add question
        res = self.client().post('questions', json=new_question)
        data = json.loads(res.data)
        newTotal = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # test that the number of questions has increased by 1
        self.assertEqual(newTotal, oldTotal+1)

    def test_add_question_failure(self):
        new_question = {
            'question': 'Who is the first man?',
            'answer': 'Adam',
            'category': 1
        }
        oldTotal = len(Question.query.all())
        
        # Add question
        res = self.client().post('questions', json=new_question)
        data = json.loads(res.data)
        newTotal = len(Question.query.all())

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Sorry, request cannot be processed")

        # test that the number of questions has not increased by 1
        self.assertEqual(newTotal, oldTotal)

    def test_question_search(self):
        query = {
            'searchTerm': 'e'
        }
        res = self.client().post('/questions/search', json=query)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_quiz(self):
        quiz = {'previous_questions': [],
                          'quiz_category': {'type': 'Test', 'id': 1}}

        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_quiz_404(self):
        quiz = {'quiz_category': {'type': 'Test', 'id': 1}}

        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Sorry, request cannot be processed")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()