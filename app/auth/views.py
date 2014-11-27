# -*- coding: utf-8 -*-
from flask.ext.login import login_user, logout_user, login_required, \
    current_user, redirect, url_for, flash
from . import auth
from .oauth import OAuthSignIn
from .. import db
from ..models import User
from ..email import send_email


# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated():
#         current_user.ping()
#         if not current_user.confirmed \
#                 and request.endpoint[:5] != 'auth.' \
#                 and request.endpoint != 'static':
#             return redirect(url_for('auth.unconfirmed'))

@auth.route('/login')
def login(provider='google'):
    if not current_user.is_anonymous():
        return redirect(url_for('main.index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@auth.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('main.index'))
    oauth = OAuthSignIn.get_provider(provider)
    id, name, family_name, email, picture, gender, locale = oauth.callback()
    if id is None:
        flash(u'A autenticação falhou.')
        return redirect(url_for('main.index'))
    user = User.query.filter_by(id=id).first()
    if not user:
        user = User(id=id,
                    name=name,
                    family_name=family_name,
                    email=email,
                    picture=picture,
                    gender=gender,
                    locale=locale)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('main.index'))

@auth.route('/logout')
@login_required
def logout():
    # session.pop('google_token', None)
    logout_user()
    flash(u'Você foi desconectado.')
    return redirect(url_for('main.index'))
