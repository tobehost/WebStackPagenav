# app/admin/views/admin_model_view.py
from flask import redirect, request, flash, url_for
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from importlib import import_module
import logging

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
    delete_template = 'admin/model/delete.html'
    
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

    def get_dao(self):
        """返回关联的 DAO 实例；优先使用已设置的 self.dao，否则按约定动态导入 app.dao.<modelname>_dao.<ModelName>DAO"""
        if getattr(self, 'dao', None):
            return self.dao

        model = getattr(self, 'model', None)
        if not model:
            return None

        module_name = f"app.dao.{model.__name__.lower()}_dao"
        class_name = f"{model.__name__}DAO"
        try:
            mod = import_module(module_name)
            dao_cls = getattr(mod, class_name, None)
            if dao_cls:
                self.dao = dao_cls()
                return self.dao
        except Exception as e:
            logging.debug("AdminModelView.get_dao: failed to import %s.%s: %s", module_name, class_name, e)
        return None

    def get_query(self):
        """优先使用 DAO 提供的查询方法（不同 DAO 可能命名不同，按常见候选名尝试），否则回退到父类实现。"""
        dao = self.get_dao()
        if dao:
            for candidate in ('get_query', 'query', 'list_query', 'get_read_query', 'get_read_session_query'):
                if hasattr(dao, candidate):
                    try:
                        return getattr(dao, candidate)()
                    except Exception:
                        logging.debug("DAO.%s call failed", candidate, exc_info=True)
        return super().get_query()

    def get_count_query(self):
        """优先使用 DAO 的计数查询/方法，否则回退到父类实现。"""
        dao = self.get_dao()
        if dao:
            for candidate in ('get_count_query', 'count_query', 'count', 'get_count'):
                if hasattr(dao, candidate):
                    try:
                        return getattr(dao, candidate)()
                    except Exception:
                        logging.debug("DAO.%s call failed", candidate, exc_info=True)
        return super().get_count_query()

    def create_model(self, form):
        """创建时优先走 DAO.create(model) 或 DAO.create_from_dict，回退到父类实现。"""
        dao = self.get_dao()
        # 尝试使用 DAO 创建
        if dao:
            try:
                # 填充 model 实例
                model = self.model()
                form.populate_obj(model)
                # 支持两类 DAO 接口：create(model) 或 create_from_dict(dict)
                if hasattr(dao, 'create'):
                    dao.create(model)
                    return True
                if hasattr(dao, 'create_from_dict'):
                    dao.create_from_dict(form.data)
                    return True
            except Exception as ex:
                self.handle_view_exception(ex)
                return False
        # 回退到父类
        return super().create_model(form)

    def update_model(self, form, model):
        """更新时优先走 DAO.update(model) 或 DAO.update_from_dict(id, dict)，否则回退。"""
        dao = self.get_dao()
        if dao:
            try:
                form.populate_obj(model)
                if hasattr(dao, 'update'):
                    dao.update(model)
                    return True
                if hasattr(dao, 'update_from_dict'):
                    key = getattr(model, 'id', None)
                    dao.update_from_dict(key, form.data)
                    return True
            except Exception as ex:
                self.handle_view_exception(ex)
                return False
        return super().update_model(form, model)

    def delete_model(self, model):
        """删除时优先走 DAO.delete(model) 或 DAO.delete_by_id(id)，否则回退。"""
        dao = self.get_dao()
        if dao:
            try:
                if hasattr(dao, 'delete'):
                    dao.delete(model)
                    return True
                if hasattr(dao, 'delete_by_id'):
                    key = getattr(model, 'id', None)
                    dao.delete_by_id(key)
                    return True
            except Exception as ex:
                self.handle_view_exception(ex)
                return False
        return super().delete_model(model)