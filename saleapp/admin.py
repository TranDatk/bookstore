from saleapp import db, app, dao
from saleapp.models import Category, Book, UserRole, Tag, RuleModel
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request
from flask_login import logout_user, current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class AuthenticatedModelViewBookSeller(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.BOOK_SELLER

class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')

        return super().__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class ProductView(AuthenticatedModelView):
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    can_view_details = True
    column_exclude_list = ['image', 'description']
    can_export = True
    column_export_list = ['id', 'name', 'description', 'price']
    column_labels = {
        'name': 'Tên sản phẩm',
        'description': 'Mô tả',
        'price': 'Giá'
    }
    page_size = 5
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }



class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats = dao.stats_revenue_by_prod(kw=request.args.get('kw'),
                                          from_date=request.args.get('from_date'),
                                          to_date=request.args.get('to_date'))
        statsbook = dao.statistic_book_using_frequency_month(keyword=request.args.get('keyword'),
                                          from_month=request.args.get('from_month'),
                                          to_month=request.args.get('to_month'))
        return self.render('admin/stats.html', stats=stats,statsbook=statsbook)

    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.ADMIN


# class StatsBookView(AuthenticatedView):
#     @expose('/')
#     def index(self):
#         stats = dao.statistic_book_using_frequency_month(kw=request.args.get('kw'),
#                                           from_date=request.args.get('from_date'),
#                                           to_date=request.args.get('to_date'))
#         return self.render('admin/stats.html', stats=stats)
#
#     def is_accessible(self):
#         return current_user.is_authenticated and \
#                current_user.user_role == UserRole.ADMIN




class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

class BookSellerView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/bookseller.html')

    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.BOOK_SELLER

class WareHouseManagerView(BaseView):
    @expose('/')

    def index(self):
        return self.render('admin/warehousemanager.html')

    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.WAREHOUSE_MANGER

class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_book_by_cate()
        return self.render('admin/index.html', stats=stats)


admin = Admin(app=app, name='Quản trị bán hàng', template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(AuthenticatedModelView(Category, db.session, name='Danh mục'))
admin.add_view(AuthenticatedModelView(Tag, db.session, name='Tag'))
admin.add_view(ProductView(Book, db.session, name='Quản trị sách'))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(BookSellerView(name='Đặt sách'))
admin.add_view(WareHouseManagerView(name='Nhập kho'))
admin.add_view(AuthenticatedModelView(RuleModel, db.session, name='Quy định'))
admin.add_view(LogoutView(name='Đăng xuất'))

