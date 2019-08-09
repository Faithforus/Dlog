from flask import render_template, url_for
from app.model.blogger import Blogger
from app.model.setting import Setting,setting_col
from app.ext import gfw
from app.lib.word_library.path import baokong,fandong,minsheng,seqing
from app import init_app

app = init_app()


@app.before_first_request
def set_blogger():
    """初始化博主"""
    b = Blogger.query.all()
    if not b:
        b = Blogger()
        error = b.new_it()
        if not error:
            print("Dlog init success!")
        else:
            print("Dlog init fail,check!please!")
    """初始化配置"""
    s = Setting.query.first()
    if s:
        for col in setting_col.keys():
            app.config[col.upper()] = getattr(s,col)
        print("系统设置加载成功!")

    gfw.parse(baokong)
    gfw.parse(fandong)
    gfw.parse(minsheng)
    gfw.parse(seqing)
    print("敏感词库加载成功！")

@app.errorhandler(404)
def miss404(e):
    return render_template('page_404.html'), 404


@app.errorhandler(405)
def miss405(e):
    return render_template('page_404.html'), 405


@app.route('/404', methods=['GET'])
def page_404():
    return render_template('page_404.html')
