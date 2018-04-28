from pyramid.view import view_config
import webpage.infrastructure.static_cache

# @view_config(route_name='home', renderer='templates/mytemplate.pt')
# def my_view(request):
#     return extend_model({'project': 'webrepo'})
#
#
# def extend_model(model_dict):
#     model_dict['build_cache_id'] = webrepo.infrastructure.static_cache.build_cache_id
#     return model_dict