from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request

class UsersModelView(ModelView):
    edit_modal = True
    can_delete = True
    page_size = 50
    can_edit = True
    column_searchable_list = ('name', 'username', 'email')
    column_list = ('name', 'username', 'about', 'content','password_hash')
    column_labels = dict(
      name='Name',
      email='Email',
      username='Username',
      password_hash='Password',
      about='About'
    )
    column_editable_list = ('name', 'username', 'email')
    form_columns = ('name', 'username', 'email', 'password_hash', 'about')

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('userbp.login', next=request.url))
    
    def on_model_change(self, form, model, is_created):    
      if form.password_hash.data:
        model.password = form.password_hash.data
      else:
        del form.password_hash
        
        
class RateModelView(ModelView):
    edit_modal = True
    can_delete = True
    page_size = 50
    can_edit = True
    column_searchable_list = ('title', 'rate_type', 'content')
    column_list = ('id','title', 'rate_type', 'date_posted')
    column_editable_list = ('title', 'rate_type')
    form_columns =  ('title', 'rate_type', 'content', 'rater')
    form_create_rules = ('title', 'rate_type', 'content', 'rater')
    form_edit_rules = ('title', 'rate_type', 'content')
    
    
class SeasonModelView(ModelView):
    edit_modal = True
    can_delete = True
    page_size = 50
    can_edit = True
    column_searchable_list = ('title', 'season', 'content')
    column_list = ('id','title', 'season', 'seasons')
    column_editable_list = ('title', 'season', 'date_posted')
    form_columns =  ('title', 'season', 'content', 'seasons')
    form_create_rules = ('title', 'season', 'content', 'seasons')
    form_edit_rules = ('title', 'season', 'content')