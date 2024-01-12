from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def root():
    pass

    """Create a task for a given queue with an arbitrary payload."""
