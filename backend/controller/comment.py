from flask import Blueprint, request, session, jsonify

from module.comment import Comment

comment=Blueprint('comment',__name__)

@comment.route('/comment',methods=['POST'])
def add():
    post_id=request.form.get('post_id')
    content=request.form.get('content').strip()
    ipaddr=request.remote_addr

    if content==None or content=='' or len(content)>200:
        return {"info": "error" ,"code": 1} #评论内容不正确

    if request.json['user_id']==None:
        return {"info": "error" ,"code": 2} #未登录

    comment=Comment()
    try:
        comment.insert_comment(post_id,content,ipaddr)
        return {"info": "success" ,"code": 0}
    except:
        return {"info": "error" ,"code": 3} #新增失败

@comment.route('/reply',methods=['POST'])
def reply():
    post_id=request.form.get('post_id')
    comment_id=request.form.get('comment_id')
    content=request.form.get('content')
    ipaddr=request.remote_addr

    #评论字数限制
    if content==None or content=='' or len(content)>200:
        return {"info": "success" ,"code": 2} #内容有错误

    if request.json['user_id'] == None:
        return {"info": "success" ,"code": 3} #未登录

    comment=Comment()
    try:
        comment.insert_reply(post_id=post_id,comment_id=comment_id,
                             content=content,ipaddr=ipaddr)
        return {"info": "success" ,"code": 0} #回复成功
    except:
        return {"info": "success" ,"code": 1} #回复失败

#为了使用ajax分页
#由于分页栏已经完成渲染，此接口仅根据前端的页码请求后台对应数据
@comment.route('/comment/<int:post_id>-<int:page>')
def comment_page(post_id,page):
    start=(page-1)*10
    comment=Comment()
    list=comment.get_comment_user_list(post_id,start,10)
    return jsonify(list)

