import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import User, Post

app = create_app()
#for flask shell
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}
