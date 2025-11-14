from flask import redirect, request, flash, url_for
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView

class AdminModelView(ModelView):
    """
    基础管理视图类，提供权限控制和通用功能
    """
    
    # 页面配置
    page_size = 20
    can_view_details = True
    can_export = True
    create_modal = False
    edit_modal = False
    details_modal = False
    
    # 模板配置 - 更新为新的路径
    list_template = 'admin/model/list.html'
    create_template = 'admin/model/create.html'
    edit_template = 'admin/model/edit.html'
    details_template = 'admin/model/details.html'
    
    def is_accessible(self):
        """检查用户是否有权限访问管理后台"""
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        """当用户无权限访问时的回调函数"""
        flash('您需要登录才能访问管理后台', 'warning')
        return redirect(url_for('auth.login', next=request.url))
    
    def on_model_change(self, form, model, is_created):
        """模型变更时的通用处理"""
        if is_created:
            self.after_model_created(form, model)
        else:
            self.after_model_updated(form, model)
    
    def after_model_created(self, form, model):
        """模型创建后的处理"""
        pass
    
    def after_model_updated(self, form, model):
        """模型更新后的处理"""
        pass
    
    def after_model_delete(self, model):
        """模型删除后的处理"""
        pass