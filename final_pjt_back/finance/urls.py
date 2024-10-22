from django.urls import path, include
from . import views

deposit_patterns = [
    path('', views.deposit_list, name='deposit_list'),
    path('<str:deposit_code>/', views.deposit_detail, name='deposit_detail'),
    path('<str:deposit_code>/Option_list/', views.depositOption_list, name='depositOption_list'),
    path('<str:deposit_code>/Option_list/<int:depositOption_pk>/', views.depositOption_detail, name='depositOption_detail'),
    path('<str:deposit_code>/like/', views.like_deposit, name='like_deposit'),
]

saving_patterns = [
    path('', views.saving_list, name='saving_list'),
    path('<str:saving_code>/', views.saving_detail, name='saving_detail'),
    path('<str:saving_code>/Option_list/', views.savingOption_list, name='savingOption_list'),
    path('<str:saving_code>/Option_list/<int:savingOption_pk>/', views.savingOption_detail, name='savingOption_detail'),
    path('<str:saving_code>/like/', views.like_saving, name='like_saving'),
]

term_deposit_patterns = [
    path('6months/', views.get_deposits, {'save_trm': '6'}, name='deposit_6months'),
    path('12months/', views.get_deposits, {'save_trm': '12'}, name='deposit_12months'),
    path('24months/', views.get_deposits, {'save_trm': '24'}, name='deposit_24months'),
    path('36months/', views.get_deposits, {'save_trm': '36'}, name='deposit_36months'),
    path('-6months/', views.get_reverse_deposits, {'save_trm': '6'}, name='reverse_deposit_6months'),
    path('-12months/', views.get_reverse_deposits, {'save_trm': '12'}, name='reverse_deposit_12months'),
    path('-24months/', views.get_reverse_deposits, {'save_trm': '24'}, name='reverse_deposit_24months'),
    path('-36months/', views.get_reverse_deposits, {'save_trm': '36'}, name='reverse_deposit_36months'),
]

term_saving_patterns = [
    path('6months/', views.get_savings, {'save_trm': '6'}, name='saving_6months'),
    path('12months/', views.get_savings, {'save_trm': '12'}, name='saving_12months'),
    path('24months/', views.get_savings, {'save_trm': '24'}, name='saving_24months'),
    path('36months/', views.get_savings, {'save_trm': '36'}, name='saving_36months'),
    path('-6months/', views.get_reverse_savings, {'save_trm': '6'}, name='reverse_saving_6months'),
    path('-12months/', views.get_reverse_savings, {'save_trm': '12'}, name='reverse_saving_12months'),
    path('-24months/', views.get_reverse_savings, {'save_trm': '24'}, name='reverse_saving_24months'),
    path('-36months/', views.get_reverse_savings, {'save_trm': '36'}, name='reverse_saving_36months'),
]

urlpatterns = [
    path('deposit_list/', include((deposit_patterns, 'deposits'))),
    path('saving_list/', include((saving_patterns, 'savings'))),
    path('deposit/', include((term_deposit_patterns, 'term_deposits'))),
    path('saving/', include((term_saving_patterns, 'term_savings'))),
    path('get_bank_deposit/<str:kor_co_nm>/', views.get_bank_deposit, name='get_bank_deposit'),
    path('get_bank_saving/<str:kor_co_nm>/', views.get_bank_saving, name='get_bank_saving'),
    path('make_financial_data/', views.make_financial_data, name='make_financial_data'),
    path('user-likes/', views.user_likes, name='user_likes'),
    path('user-likes2/', views.user_likes2, name='user_likes'),
    path('remove_like/<int:product_id>/<int:user_id>', views.user_likes_delete, name='user_likes_delete'),
    path('remove_like2/<int:product_id>/<int:user_id>', views.user_likes2_delete, name='user_likes_delete'),

]

