from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

url_prefix = '/services'
bp = Blueprint('services', __name__)
