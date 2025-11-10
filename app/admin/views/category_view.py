from flask import flash
from wtforms import TextAreaField
from app.admin.views.admin_model_view import AdminModelView
from app.models import Category

class CategoryView(AdminModelView):
    """
    分类管理视图
    """
    
    # 列配置
    column_list = ('name', 'icon', 'description', 'sort_order', 'is_active', 'created_at', 'link_count')
    column_labels = {
        'name': '分类名称',
        'icon': '图标',
        'description': '描述',
        'sort_order': '排序',
        'is_active': '是否激活',
        'created_at': '创建时间',
        'link_count': '链接数量'
    }
    column_sortable_list = ('name', 'sort_order', 'is_active', 'created_at')
    column_searchable_list = ('name', 'description')
    column_filters = ('is_active', 'created_at')
    column_default_sort = ('sort_order', True)
    
    # 表单配置
    form_columns = ('name', 'icon', 'description', 'sort_order', 'is_active')
    form_extra_fields = {
        'description': TextAreaField('描述')
    }
    form_choices = {
        'icon': [
            ('linecons-star', '星星'),
            ('linecons-doc', '文档'),
            ('linecons-lightbulb', '灯泡'),
            ('linecons-thumbs-up', '点赞'),
            ('linecons-diamond', '钻石'),
            ('linecons-pencil', '铅笔'),
            ('linecons-user', '用户'),
            ('linecons-heart', '爱心'),
            ('linecons-tag', '标签'),
            ('linecons-cog', '设置')
        ]
    }
    
    # 模板配置
    list_template = 'admin/category/list.html'
    create_template = 'admin/category/create.html'
    edit_template = 'admin/category/edit.html'
    
    def get_query(self):
        """获取查询对象"""
        return super().get_query()
      
    def get_count_query(self):
        """获取计数查询"""
        return super().get_count_query()
    
    def scaffold_list_columns(self):
        """构建列表列"""
        columns = super().scaffold_list_columns()
        # 添加链接数量列
        if 'link_count' not in columns:
            columns.append('link_count')
        return columns
    
    def after_model_created(self, form, model):
        """分类创建后的处理"""
        flash(f'分类 "{model.name}" 创建成功', 'success')
    
    def after_model_updated(self, form, model):
        """分类更新后的处理"""
        flash(f'分类 "{model.name}" 更新成功', 'success')
    
    def after_model_delete(self, model):
        """分类删除后的处理"""
        flash(f'分类 "{model.name}" 删除成功', 'success')
    
    def on_model_delete(self, model):
        """分类删除前的处理"""
        # 检查是否有关联的链接
        if model.links:
            flash(f'无法删除分类 "{model.name}"，因为还有 {len(model.links)} 个链接关联到此分类', 'error')
            return False
        return True