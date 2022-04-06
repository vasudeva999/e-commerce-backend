from flask_server import app
from flask_graphql import GraphQLView
from config.schema import schema

app.add_url_rule('/',
                 view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
