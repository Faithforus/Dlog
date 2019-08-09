import json

from flask import render_template, request, jsonify, redirect, url_for, current_app
from sqlalchemy import func, and_

from app.view.index import index_bp
from app.model import db
from app.model.blog import Blog
from app.model.comment import Comment
from app.lib.common import trueReturn, falseReturn
from app.ext import limiter



@index_bp.route('/', methods=['GET', 'POST'])
@limiter.exempt
def index():
    """

    :return: category:[(category,sum)]
    """
    category = db.session.query(Blog.category, func.count(Blog.blog_id)).group_by(Blog.category)
    home_page = current_app.config.get('HOME_PAGE', 'Dlog Home Page')
    # home_comment = db.session.query(Comment.guest_name, Comment.comment, Comment.create_time).filter_by(
    #     blog_id="home-tab").all()
    page_index =  current_app.config['PAGE_SIZE']
    page_size = 3
    current_app.config['PAGE_SIZE']+=1
    home_comment = db.session.query(Comment.guest_name, Comment.comment, Comment.create_time).filter_by(
        blog_id="home-tab").limit(page_size).offset((page_index - 1) * page_size)

    data = []
    if home_comment:
        for result in home_comment:
            temp = {}
            for key, res in zip(result.keys(), result):
                if key == "create_time":
                    temp[key] = res.strftime("%Y年 %m月 %d日 %H时:%M分")
                else:
                    temp[key] = res
            data.append(temp)  # [{},{}]
    return render_template('index.html', category=category, home_page=home_page, home_comment=data,
                           home_count=len(data))


@index_bp.route('/get_blog_list', methods=['POST'])
def get_blog_list():
    """

    :return: results：[(blog_id,title,create_time),(blog_id,title,create_time)]
    """
    code = request.values.get('code')
    results = db.session.query(Blog.blog_id, Blog.title, Blog.create_time).filter_by(category=code).order_by(
        Blog.create_time).all()
    if not results:
        return jsonify(falseReturn(msg='暂无文章'))
    data = []
    for result in results:
        temp = {}
        for key, res in zip(result.keys(), result):
            if key == "create_time":
                temp[key] = res.strftime("%Y年 %m月 %d日 %H时:%M分")
            else:
                temp[key] = res
        data.append(temp)
    return jsonify(trueReturn(data=data))


@index_bp.route('/get_blog_detail', methods=['POST'])
@limiter.limit("100 per day")
def get_blog_detail():
    """
    # data = [dict(zip(result.keys(), result)) for result in results]
    # print(data)
    :return: ('','')
    """
    code = request.values.get('code')
    """博客内容"""
    bolg_title = db.session.query(Blog.body_html).filter_by(blog_id=code).first()
    if not bolg_title:
        return jsonify(falseReturn(msg="出错了～"))
    """评论内容"""
    comment = db.session.query(Comment.guest_name, Comment.comment, Comment.create_time).filter(
        and_(Comment.blog_id == code, Comment.display == True)).all()
    data = []

    if comment:
        for result in comment:
            temp = {}
            for key, res in zip(result.keys(), result):
                if key == "create_time":
                    temp[key] = res.strftime("%Y年 %m月 %d日 %H时:%M分")
                else:
                    temp[key] = res
            data.append(temp)
    return jsonify(trueReturn(data={"bolg_title": bolg_title, "comment": data, "comment_count": len(data)}))


@index_bp.route('/search', methods=['GET', 'POST'])
def search():
    keyword = request.values.get('keyword')
    results = db.session.query(Blog.blog_id, Blog.title, Blog.create_time).filter(Blog.title.like(keyword)).all()
    if not results:
        return jsonify(falseReturn(msg='^_^||没有找到你要的东西～'))
    data = []
    for result in results:
        temp = {}
        for key, res in zip(result.keys(), result):
            if key == "create_time":
                temp[key] = res.strftime("%Y年 %m月 %d日 %H时:%M分")
            else:
                temp[key] = res
        data.append(temp)
    return jsonify(trueReturn(data=data))
