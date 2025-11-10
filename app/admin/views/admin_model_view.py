from flask import redirect, request, flash
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
    create_modal = True
    edit_modal = True
    details_modal = True
    
    def is_accessible(self):
        """检查用户是否有权限访问"""
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        """无权限访问时的回调"""
        flash('您没有权限访问此页面', 'error')
        return redirect('/admin/login')
    
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
    
    def get_empty_list_message(self):
        """空列表时的提示信息"""
        return "暂无数据"
    
    def get_list_columns(self):
        """获取列表显示的列"""
        return super().get_list_columns()

    # CRUD 操作统一在此处理，具体视图可以只实现钩子方法
    def create_model(self, form):
        """创建模型并提交到数据库，调用 after_model_created 钩子"""
        try:
            model = self.model()
            form.populate_obj(model)
            self.session.add(model)
            self.session.commit()
            try:
                self.after_model_created(form, model)
            except Exception:
                # 钩子不应影响主流程，记录并继续
                pass
            return True
        except Exception as ex:
            self.session.rollback()
            flash(f'创建失败: {ex}', 'error')
            return False

    def update_model(self, form, model):
        """更新模型并提交到数据库，调用 after_model_updated 钩子"""
        try:
            form.populate_obj(model)
            self.session.add(model)
            self.session.commit()
            try:
                self.after_model_updated(form, model)
            except Exception:
                pass
            return True
        except Exception as ex:
            self.session.rollback()
            flash(f'更新失败: {ex}', 'error')
            return False

    def delete_model(self, model):
        """删除模型前后调用钩子并提交变更"""
        try:
            # 先调用 before-delete 检查（如果实现为 on_model_delete）
            try:
                ok = True
                if hasattr(self, 'on_model_delete'):
                    ok = self.on_model_delete(model)
                if ok is False:
                    return False
            except Exception as e:
                # 如果检查抛出异常，阻止删除并提示
                flash(f'删除前检查失败: {e}', 'error')
                return False

            self.session.delete(model)
            self.session.commit()
            try:
                self.after_model_delete(model)
            except Exception:
                pass
            return True
        except Exception as ex:
            self.session.rollback()
            flash(f'删除失败: {ex}', 'error')
            return False
