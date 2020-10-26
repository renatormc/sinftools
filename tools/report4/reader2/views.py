from flask import Blueprint, render_template, session, request, redirect
from models import *
from database import db_session

views = Blueprint('views', __name__)


@views.route("/")
def index():
    return render_template("base.html")
