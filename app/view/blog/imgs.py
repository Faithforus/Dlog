import os
import time
from flask import request, url_for, jsonify,current_app
from flask_login import login_required
from PIL import Image

from app.ext import photos
from app.view.blog import blog_bp
from app.lib.common import trueReturn, falseReturn

@login_required
@blog_bp.route('/uploads', methods=['POST'])
def uploads():
    photo = request.files.get('editormd-image-file')
    if request.method == 'POST' and photo:
        # 时间戳做文件名
        suffix = os.path.splitext(photo.filename)[1]
        filename = str(int(time.time())) + suffix
        # 保存
        photos.save(photo, name=filename)
        # 生成缩略图
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],
                                filename)
        # 1.打开文件
        img = Image.open(pathname)
        # 2.设置尺寸
        img.thumbnail((320, 320))
        # 3.保存,覆盖原图
        img.save(pathname)
        img_url = photos.url(filename)
        res = {
            'success': 1,
            'message': '上传成功',
            'url': img_url
        }
    else:
        res = {
            'success': 0,
            'message': '上传失败'
        }
    return jsonify(res)
