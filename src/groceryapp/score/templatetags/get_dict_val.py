from django.template.defaulttags import register

@register.filter
def get_dict_val(dictionaty,key,key_as_str=True):
    if not isinstance(dictionaty,dict):
        return None
    if key_as_str:
        key=f"{key}"
    return dictionaty.get(key)