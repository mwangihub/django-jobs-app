from django import template
register = template.Library()
@register.filter
def account_type(user):
    tag = None
    if user.is_admin and user.is_staff:
        tag = 'Administrator account'
    if user.is_staff and not user.is_admin:
        tag = 'Staff account'
    if user.is_employee:
        tag = 'Employee account'
    if user.is_buyer:
        tag = 'Buyer account'
    if user.is_non:
        tag = 'Select account type'
    return tag