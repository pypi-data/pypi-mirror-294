from action_set_lib.utils.contact_tool import redis_add_contact, redis_show_contact

def add_contact(name, address, **kwargs):
    redis_client = kwargs.get('redis_client')
    executor =  kwargs.get('executor')
    return redis_add_contact(redis_client, executor, name, address)

def show_contact_by_name(name, **kwargs):
    redis_client = kwargs.get('redis_client')
    executor =  kwargs.get('executor')
    return redis_show_contact(redis_client, executor, name)

def show_all_contact(**kwargs):
    redis_client = kwargs.get('redis_client')
    executor =  kwargs.get('executor')
    return redis_show_contact(redis_client, executor, None)