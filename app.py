import sys 
from flask import Flask , render_template , request , redirect , url_for , jsonify , abort # Flask is a class enables us to create app 
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
app = Flask(__name__)  # creating an app named with the file name ( app.py)
db = SQLAlchemy(app) #defining db object which links SQL alchemy to our flask app 
migrate = Migrate(app,db) # making an instance of Migrate Class and link it to the app and DB
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:password@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer , primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed =db.Column(db.Boolean, nullable=False , default=False)
  #to define dander-repr method for debugging purposes 
    def __repr__(self):
        return f'<ID: {self.id}, description: {self.description}>'

#db.create_all()   # to create all the tables for the created model 

@app.route('/')  # define a route to the home page , index() is the route handler 
def index():
   return render_template('index.html', data= Todo.query.order_by('id').all()
           ) #render the html page whenever the usre naviage to the home




@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_complete_todo(todo_id):
   try:
    completed = request.get_json()['completed']
    print('completed', completed)
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
   except:
    db.session.rollback()
   finally:
    db.session.close()
    return redirect(url_for('index'))


@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
   try:
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
   except:
    db.session.rollback()
   finally:
    db.session.close()
    return redirect(url_for('index'))



















@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body ={ }
    try:
       description = request.get_json()['description']
       item1 = Todo(description=description)
       db.session.add(item1)
       db.session.commit()
       body['description']= item1.description
    except: 
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if  error:
        abort(400)
    else:

        return jsonify(body)










'''
@app.route('/todos/create', methods=['POST'])
def create_todo():
    description = request.form.get('description')
    item1 = Todo(description=description)
    db.session.add(item1)
    db.session.commit()
    return redirect(url_for('index'))
''' 


#item1 = Todo(description='workout')
#item2 = Todo(description='breakfast')
#item3 = Todo(description='study')

#intiating an object from class Perosn
#db.session.add(item1)
#db.session.commit()