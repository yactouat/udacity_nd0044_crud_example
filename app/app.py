import sys
from flask import (
  abort,
  jsonify,
  render_template,
  request,
  flash,
  redirect, url_for
)
import logging
from logging import Formatter, FileHandler
from sqlalchemy import create_engine, text
from sqlalchemy.orm import load_only
from forms import *
from init import app, csrf
from models import *
from jinja_filters import format_datetime

app.jinja_env.filters['datetime'] = format_datetime


@app.route('/status')
def status():
    responseBody = {}
    error = False
    try:
        eng = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
        conn = eng.connect()
        conn.close()
        responseBody['msg'] = "database is up"
    except Exception as e:
        error = True
        responseBody['msg'] = "database is down !"
        print(sys.exc_info())
    finally:
        if error:
            return jsonify(responseBody), 500
        else:
            return jsonify(responseBody), 200


@app.route('/')
def index():
    return render_template('pages/home.html')


#  TypeBLists
#  ----------------------------------------------------------------

@app.route('/typeblists')
def typeblists():
    form = TypeBListForm()
    typeblists = (
      db.session.query(TypeBList)
      .distinct().all()
    )
    db.session.commit()
    results = []
    typeblistsFormatted = []
    for typeblist in typeblists:
        num_upcoming_items = db.session.query(Item).join(TypeBList).filter(
            Item.typeblist_id == typeblist.id
        ).filter(
            Item.start_time > datetime.now()
        ).count()
        typeblistsFormatted.append({
            "id": typeblist.id,
            "name": typeblist.name,
            "num_upcoming_items": num_upcoming_items
        })
    results.append({
        "typeblists": typeblistsFormatted
    })
    return render_template('pages/typeblists.html', results=results, form=form)


@app.route('/typeblists/search', methods=['POST'])
def search_typeblists():
    form = TypeBListForm()
    search_term = request.form.get('search_term', '')
    typeblists = TypeBList.query.filter(TypeBList.name.ilike('%'+search_term+'%')).all()
    response = {
      "count": 0,
      "data": []
    }
    for typeblist in typeblists:
        response["count"] += 1
        response["data"].append(typeblist)
    return render_template(
      'pages/search_typeblists.html',
      results=response, search_term=search_term, form=form
    )


@app.route('/typeblists/<int:typeblist_id>')
def item_typeblist(typeblist_id):
    form = TypeBListForm()
    # items the typeblist page with the given typeblist_id
    typeblist = TypeBList.query.filter_by(id=typeblist_id).first_or_404()
    return render_template('pages/item_typeblist.html', typeblist=typeblist, form=form)


@app.route('/typeblists/create', methods=['GET'])
def create_typeblist_form():
    form = TypeBListForm()
    return render_template('forms/new_typeblist.html', form=form)


@app.route('/typeblists/create', methods=['POST'])
def create_typeblist_submission():
    form = TypeBListForm()
    if form.validate_on_submit():
        try:
            typeblist = TypeBList(
              name=form.name.data,
            )
            db.session.add(typeblist)
            db.session.commit()
            # on successful db insert, flash success
            flash('TypeBList ' + typeblist.name + ' was successfully listed!')
            db.session.close()
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            db.session.close()
            flash(
              'An error occurred. TypeBList ' +
              request.form.get("name") +
              ' could not be listed.'
            )
            return render_template('forms/new_typeblist.html', form=form)
    else:
        flash(form.errors)
        return render_template('forms/new_typeblist.html', form=form)


@app.route('/typeblists/<typeblist_id>', methods=['DELETE'])
@csrf.exempt
def delete_typeblist(typeblist_id):
    responseBody = {}
    error = False
    try:
        Item.query.filter_by(typeblist_id=typeblist_id).delete()
        TypeBList.query.filter_by(id=typeblist_id).delete()
        db.session.commit()
        responseBody['msg'] = "typeblist has been deleted !"
    except Exception as e:      
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()           
        if error:
            abort(400)
        else:           
            return jsonify(responseBody)
    # TODO BONUS CHALLENGE:
    # Implement a button to delete a TypeBList on a TypeBList Page,
    # have it so that clicking that button
    # deletes it from the db then redirect the user to the homepage


@app.route('/typealists')
def typealists():
    form = TypeAListForm()
    typealists = TypeAList.query.all()
    return render_template('pages/typealists.html', typealists=typealists, form=form)


@app.route('/typealists/search', methods=['POST'])
def search_typealists():
    form = TypeAListForm()
    search_term = request.form.get('search_term', '')
    typealists = TypeAList.query.filter(TypeAList.name.ilike('%'+search_term+'%')).all()
    response = {
      "count": 0,
      "data": []
    }
    for typealist in typealists:
        num_upcoming_items = db.session.query(Item).join(TypeAList).filter(
            Item.typealist_id == typealist.id
        ).filter(
            Item.start_time > datetime.now()
        ).count()
        response["count"] += 1
        response["data"].append({
          "id": typealist.id,
          "name": typealist.name,
          "num_upcoming_items": num_upcoming_items
        })
    return render_template(
      'pages/search_typealists.html',
      results=response,
      search_term=search_term,
      form=form
    )


@app.route('/typealists/<int:typealist_id>')
def item_typealist(typealist_id):
    form = TypeAListEditForm()
    # items the typealist page with the given typealist_id
    typealist = TypeAList.query.filter_by(id=typealist_id).first_or_404()
    return render_template('pages/item_typealist.html', typealist=typealist, form=form)


@app.route('/typealists/<int:typealist_id>/edit', methods=['GET'])
def edit_typealist(typealist_id):
    form = TypeAListEditForm()
    typealist = TypeAList.query.filter_by(id=typealist_id).first_or_404()
    return render_template('forms/edit_typealist.html', form=form, typealist=typealist)


@app.route('/typealists/<int:typealist_id>/edit', methods=['POST'])
def edit_typealist_submission(typealist_id):
    form = TypeAListEditForm()
    if form.validate_on_submit():
        try:
            typealist = TypeAList.query.filter_by(id=typealist_id).first_or_404()
            typealist.name = form.name.data
            typealist.options = form.options.data
            db.session.commit()
            # on successful db insert, flash success
            flash('TypeAList ' + typealist.name + ' was successfully updated!')
            db.session.close()
            return redirect(url_for('item_typealist', typealist_id=typealist_id))
        except Exception as e:
            db.session.rollback()
            db.session.close()
            flash(
              'An error occurred. TypeAList ' + 
              request.form.get("name") + 
              ' could not be updated.'
            )
            return render_template('forms/edit_typealist.html', form=form)
    else:
        flash(form.errors)
        return render_template('forms/edit_typealist.html', form=form)


@app.route('/typeblists/<int:typeblist_id>/edit', methods=['GET'])
def edit_typeblist(typeblist_id):
    form = TypeBListEditForm()
    typeblist = TypeBList.query.filter_by(id=typeblist_id).first_or_404()
    return render_template('forms/edit_typeblist.html', form=form, typeblist=typeblist)


@app.route('/typeblists/<int:typeblist_id>/edit', methods=['POST'])
def edit_typeblist_submission(typeblist_id):
    form = TypeBListEditForm()
    if form.validate_on_submit():
        try:
            typeblist = TypeBList.query.filter_by(id=typeblist_id).first_or_404()
            typeblist.name = form.name.data
            db.session.commit()
            # on successful db insert, flash success
            flash('TypeBList ' + typeblist.name + ' was successfully updated!')
            db.session.close()
            return redirect(url_for('item_typeblist', typeblist_id=typeblist_id))
        except Exception as e:
            db.session.rollback()
            db.session.close()
            flash(
              'An error occurred. TypeBList ' +
              request.form.get("name") +
              ' could not be updated.')
            return render_template('forms/edit_typeblist.html', form=form)
    else:
        flash(form.errors)
        return render_template('forms/edit_typeblist.html', form=form)


@app.route('/typealists/create', methods=['GET'])
def create_typealist_form():
    form = TypeAListForm()
    return render_template('forms/new_typealist.html', form=form)


@app.route('/typealists/create', methods=['POST'])
def create_typealist_submission():
    form = TypeAListForm()
    if form.validate_on_submit():
        try:
            typealist = TypeAList(
              name=form.name.data,
              options=form.options.data,
            )
            db.session.add(typealist)
            db.session.commit()
            # on successful db insert, flash success
            flash('TypeAList ' + typealist.name + ' was successfully listed!')
            db.session.close()
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            db.session.close()
            flash(
              'An error occurred. TypeAList ' +
              request.form.get("name") +
              ' could not be listed.')
            return render_template('forms/new_typealist.html', form=form)
    else:
        flash(form.errors)
        return render_template('forms/new_typealist.html', form=form)


@app.route('/items')
def items():
    items = Item.query.all()
    return render_template('pages/items.html', items=items)


@app.route('/items/create')
def create_items():
    # renders form. do not touch.
    form = ItemForm()
    return render_template('forms/new_item.html', form=form)


@app.route('/items/create', methods=['POST'])
def create_item_submission():
    form = ItemForm()
    if form.validate_on_submit():
        try:
            item = Item(
              typealist_id=form.typealist_id.data, 
              typeblist_id=form.typeblist_id.data, 
              start_time=form.start_time.data
            )
            db.session.add(item)
            db.session.commit()
            # on successful db insert, flash success
            flash('Item was successfully listed!')
            db.session.close()
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            db.session.close()
            flash('An error occurred. Item could not be listed.')
            return render_template('forms/new_item.html', form=form)
    else:
        flash(form.errors)
        return render_template('forms/new_item.html', form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
          '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == '__main__':
    app.run()
# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
