from flask_server import app
from .database import db_session
from flask_graphql_auth import GraphQLAuth

app.config['JWT_SECRET_KEY'] = 'c7755034e0b788b8d751b29065e8415bd47cce8428aeee0aea9b55f0bfc43b5a'
app.config['REFRESH_EXP_LENGTH'] = 30
app.config['ACCESS_EXP_LENGTH'] = 10
app.config['JWT_SECRET_KEY'] = 'Bearer'

auth = GraphQLAuth(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()