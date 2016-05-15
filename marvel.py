# -*- coding: utf-8 -*-

# ALL THE IMPORTS!
import sqlite3
from flask import Flask, request, g, redirect, url_for, render_template
from scrape import *
from db import *
from playhouse.shortcuts import model_to_dict
from playhouse.postgres_ext import Match
from contextlib import closing

app = Flask(__name__)



def init_db():
    db.connect()
    db.create_tables([Comic, Issue])
    db.close()

app.jinja_env.globals.update(get_url=get_url)


@app.template_filter('scraped')
def bool_filter(i):
    scraped = bool(i)
    if scraped:
        return "✓"
    else:
        return "✗"

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    if number == 1: return singular
    else: return plural

@app.template_filter('parseyear')
def parse_year(year):
    if year == 0: return 'Present'
    return year


@app.before_request
def before_request():
    g.db = db
    g.db.connect()

@app.teardown_request
def teardown_request(exception):
    g.db.close()



@app.route('/')
def show_front():
    return render_template('frontpage.html')

@app.route('/titles')
def show_titles():
    titles = (Comic
              .select()
              .dicts())
    return render_template('show_titles.html', titles=titles)

@app.route('/synced')
def show_synced():
    titles = (Comic
              .select()
              .where(Comic.scraped == True)
              .dicts())
    return render_template('show_titles.html', titles=titles, synced=True)

@app.route('/search')
def show_search():
    tcount = Comic.select().count()
    icount = Issue.select().count()
    if request.query_string:
        search = request.args.get('q')
        advanced = request.args.get('adv')
        if advanced == 'on':
            query = (Comic
                     .select()
                     .where(Comic.search_title.match(search))
                     .dicts())
        else:
            query = (Comic
                     .select()
                     .where(Expression(Comic.search_title, 'T@@', fn.plainto_tsquery(search)))
                     .dicts())
        return render_template('show_search.html', totals=(tcount, icount), results=query, search=True, query=search, adv=advanced)

    return render_template('show_search.html', totals=(tcount, icount))

@app.route('/title/<int:title_id>')
def title_by_id(title_id):
    title = Comic.get(Comic.id == title_id)
    query = (Issue
             .select(Issue, Comic)
             .join(Comic)
             .order_by(Issue.num)
             .where(Issue.series == title_id))
    issues = [model_to_dict(row) for row in query]
    return render_template('show_titles_id.html', title=model_to_dict(title), issues=issues)


@app.route('/refresh/titles')
def refresh_titles():
    Comic.delete().execute()
    titles = scrape_titles()
    titles = list(map(lambda x: dict({'search_title': fn.to_tsvector(x['title'])}, **x), titles))

    with db.atomic():
        for idx in range(0, len(titles), 150):
            Comic.insert_many(titles[idx:idx+150]).execute()

    return redirect(url_for('show_titles'))

@app.route('/refresh/issues/<int:title_id>')
def refresh_issues(title_id):
    Issue.delete().where(Issue.series == title_id).execute()
    comic = Comic.get(Comic.id == title_id)
    issues = scrape_issues(model_to_dict(comic))
    issues = list(map(lambda x: dict({'series': comic}, **x), issues))

    with db.atomic():
        for idx in range(0, len(issues), 199):
            Issue.insert_many(issues[idx:idx+199]).execute()
            Comic.update(scraped=True).where(Comic.id == title_id).execute()
    return redirect(url_for('title_by_id', title_id=title_id))

if __name__ == "__main__":
    app.run(debug=True)