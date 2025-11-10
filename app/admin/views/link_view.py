from flask import flash
from wtforms import TextAreaField, URLField
from app.admin.views.admin_model_view import AdminModelView
from app.models import Link, Category

class LinkView(AdminModelView):
    """
    链接管理视图
    """
    
    # 列配置
    column_list = ('title', 'category', 'url', 'is_active', 'is_hot', 'sort_order', 'created_at')
    column_labels = {
        'title': '标题',
        'category': '分类',
        'url': '链接地址',
        'description': '描述',
        'logo': '图标',
        'sort_order': '排序',
        'is_active': '是否激活',
        'is_hot': '热门推荐',
        'created_at': '创建时间'
    }
    column_sortable_list = ('title', 'sort_order', 'is_active', 'is_hot', 'created_at')
    column_searchable_list = ('title', 'url', 'description')
    column_filters = ('is_active', 'is_hot', 'category', 'created_at')
    column_default_sort = ('sort_order', True)
    
    # 表单配置
    form_columns = ('title', 'url', 'description', 'logo', 'category', 'sort_order', 'is_active', 'is_hot')
    form_extra_fields = {
        'description': TextAreaField('描述'),
        'url': URLField('链接地址', render_kw={"placeholder": "https://example.com"})
    }
    form_ajax_refs = {
        'category': {
            'fields': ['name'],
            'page_size': 10
        }
    }
    
    # 模板配置
    list_template = 'admin/link/list.html'
    create_template = 'admin/link/create.html'
    edit_template = 'admin/link/edit.html'
    
    def get_query(self):
        """获取查询对象"""
        return super().get_query()
    
    def get_count_query(self):
        """获取计数查询"""
        return super().get_count_query()
    
    def after_model_created(self, form, model):
        """链接创建后的处理"""
        flash(f'链接 "{model.title}" 创建成功', 'success')
    
    def after_model_updated(self, form, model):
        """链接更新后的处理"""
        flash(f'链接 "{model.title}" 更新成功', 'success')
    
    def after_model_delete(self, model):
        """链接删除后的处理"""
        flash(f'链接 "{model.title}" 删除成功', 'success')
    
    def on_form_prefill(self, form, id):
        """表单预填充时的处理"""
        # 可以在这里对表单进行额外的处理
        pass