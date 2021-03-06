import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins.
  Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"/*": {"origins": '*'}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,-Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # '''
    # @TODO:
    # Create an endpoint to handle GET requests
    # for all available categories.
    # '''
    @app.route('/categories', methods=['GET'])
    def categories():
        return jsonify({
            'success': True,
            'categories':
            {category.id: category.type for category in Category.query.all()}
        })

    # '''
    # @TODO:
    # Create an endpoint to handle GET requests for questions,
    # including pagination (every 10 questions).
    # This endpoint should return a list of questions,
    # number of total questions, current category, categories.

    # TEST: At this point, when you start the application
    # you should see questions and categories generated,
    # ten questions per page and pagination
    # at the bottom of the screen for three pages.
    # Clicking on the page numbers should update the questions.
    # '''
    RESULTS_PER_PAGE = 10

    def paginate_selection(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * RESULTS_PER_PAGE
        end = start + RESULTS_PER_PAGE

        # get all results
        filtered = [question.format for question in selection]
        result = filtered[start:end]

        return result

    @app.route('/questions', methods=['GET'])
    def questions():
        selection = Question.query.order_by(Question.id).all()
        questions = paginate_selection(request, selection)
        if len(questions) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(selection),
            'current_category': None,
            'categories':
            {category.id: category.type for category in Category.query.all()},
            'total': len(Question.query.all())
        })

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question,
  the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
        except:
            abort(404)
        return jsonify({
            'success': True
        })

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.json
        if 'question' in body and 'answer' in body \
                and 'category' in body and 'difficulty' in body:
            question_body = body['question']
            answer = body['answer']
            category = body['category']
            difficulty = body['difficulty']

            question = Question(question_body, answer, category, difficulty)
            question.insert()
            return jsonify({
                'success': True,
                'question': question.id
            })
        else:
            abort(422)

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        if 'searchTerm' in body:
            query = body['searchTerm']
            results = Question.query.filter(
                Question.question.ilike('%' + query + '%')).all()
            paginated = paginate_selection(request, results)
            return jsonify({
                'success': True,
                'questions': paginated,
                'total_questions': len(Question.query.all()),
                'current_category': None
            })
        else:
            abort(404)

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def category_questions(category_id):
        try:
            questions = Question.query.filter(
                Question.category == category_id).all()
            if len(questions) == 0:
                abort(404)
            results = paginate_selection(request, questions)
            return jsonify({
                'success': True,
                'category': category_id,
                'questions': results,
                'question_count': len(results),
                'total': len(Question.query.all())
            })
        except:
            abort(404)

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.json
        if 'quiz_category' in body and 'previous_questions' in body:
            category = body['quiz_category']
            print(category)
            previous = body['previous_questions']
            print(previous)
            category_type = category['type']
            # print(category_type)
            # print(previous)
            if category_type == 'click':
                questions = Question.query.filter(
                    Question.id.notin_(previous)).all()
            else:
                questions = Question.query\
                    .filter_by(category=category['id'])\
                    .filter(Question.id.notin_(previous)).all()

            question = questions[random.randrange(0, len(questions))]\
                .format if len(questions) > 0 else None
            # print(questions)
            # print(question)
            return jsonify({
                'success': True,
                'question': question
            })
        else:
            abort(422)

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Sorry, resource unavailable"
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Sorry, request cannot be processed"
        }), 422

    return app
