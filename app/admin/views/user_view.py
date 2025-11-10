from flask import flash
from wtforms import PasswordField, validators
from app.admin.views.admin_model_view import AdminModelView
from app.models import User

class UserView(AdminModelView):
    """
    用户管理视图
    """
    
    # 列配置
    column_list = ('username', 'own_reset', 'is_admin', 'created_at')
    column_labels = {
        'username': '用户名',
        'own_reset': '找回密码凭证',
        'is_admin': '是否管理员',
        'created_at': '创建时间'
    }
    column_descriptions = {
        'own_reset': '预设密码是找回密码的凭证，限定为6位数字'
    }
    column_sortable_list = ('username', 'is_admin', 'created_at')
    column_searchable_list = ('username',)
    column_filters = ('is_admin', 'created_at')
    
    # 表单配置
    form_columns = ('username', 'password', 'own_reset', 'is_admin')
    form_extra_fields = {
        'password': PasswordField('密码', validators=[
            validators.DataRequired(),
            validators.Length(min=6, message='密码长度至少6位')
        ])
    }
    form_args = {
        'own_reset': {
            'validators': [
                validators.DataRequired(message='找回密码凭证不能为空'),
                validators.Regexp('^[0-9]{6}$', message='找回密码凭证必须是6位数字')
            ]
        }
    }
    
    # 模板配置
    list_template = 'admin/user/list.html'
    create_template = 'admin/user/create.html'
    edit_template = 'admin/user/edit.html'
    
    def scaffold_form(self):
        """构建表单"""
        form_class = super().scaffold_form()
        return form_class
    
    def on_model_change(self, form, model, is_created):
        """模型变更时的处理"""
        # 处理密码
        if form.password.data:
            model.set_password(form.password.data)
        
        super().on_model_change(form, model, is_created)
    
    def after_model_created(self, form, model):
        """用户创建后的处理"""
        flash(f'用户 "{model.username}" 创建成功', 'success')
    
    def after_model_updated(self, form, model):
        """用户更新后的处理"""
        flash(f'用户 "{model.username}" 更新成功', 'success')
    
    def after_model_delete(self, model):
        """用户删除后的处理"""
        flash(f'用户 "{model.username}" 删除成功', 'success')
    
    def on_model_delete(self, model):
        """用户删除前的处理"""
        # 防止删除当前登录用户
        from flask_login import current_user
        if model.id == current_user.id:
            flash('不能删除当前登录的用户', 'error')
            return False
        return True