import json
import os
import inspect
import re
import pathlib
from django.template import Template, Context
from django.apps import apps
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.http import HttpResponse

from django.db.models import OneToOneRel, ManyToOneRel, ManyToManyRel # reverse 
from django.db.models import OneToOneField, ForeignKey, ManyToManyField # forward


class ShowModelsAll(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if 'code_device' not in request.session:
            request.session['code_device'] = 'vs'
            
        if 'OneToOneField_text' not in request.session:
            request.session['OneToOneField_text'] = '#f8fafc'
        if 'OneToOneField_bg' not in request.session:
            request.session['OneToOneField_bg'] = '#86198f'
            
        if 'ForeignKey_text' not in request.session:
            request.session['ForeignKey_text'] = '#f8fafc'
        if 'ForeignKey_bg' not in request.session:
            request.session['ForeignKey_bg'] = '#86198f'
            
        if 'ManyToManyField_text' not in request.session:
            request.session['ManyToManyField_text'] = '#f8fafc'
        if 'ManyToManyField_bg' not in request.session:
            request.session['ManyToManyField_bg'] = '#86198f'
            
        if 'OneToOneRel_text' not in request.session:
            request.session['OneToOneRel_text'] = '#f8fafc'
        if 'OneToOneRel_bg' not in request.session:
            request.session['OneToOneRel_bg'] = '#9a3412'
            
        if 'ManyToOneRel_text' not in request.session:
            request.session['ManyToOneRel_text'] = '#f8fafc'
        if 'ManyToOneRel_bg' not in request.session:
            request.session['ManyToOneRel_bg'] = '#9a3412'
            
        if 'ManyToManyRel_text' not in request.session:
            request.session['ManyToManyRel_text'] = '#f8fafc'
        if 'ManyToManyRel_bg' not in request.session:
            request.session['ManyToManyRel_bg'] = '#9a3412'
            
        if 'selected_text' not in request.session:
            request.session['selected_text'] = '#f8fafc'
        if 'selected_bg' not in request.session:
            request.session['selected_bg'] = '#166534'
            
        if 'default_text' not in request.session:
            request.session['default_text'] = '#f8fafc'
        if 'default_bg' not in request.session:
            request.session['default_bg'] = '#1E429F'
        
        if 'method_text' not in request.session:
            request.session['method_text'] = '#f8fafc'
        if 'method_bg' not in request.session:
            request.session['method_bg'] = '#115e59'
            
        return super().dispatch(request, *args, **kwargs)
                
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["models"] = json.dumps(self.get_models_data())
        context['session'] = self.request.session
        return context

    def get_models_data(self):
        models_data = []
        list_of_models = apps.get_models()

        for model in list_of_models:
            model_info = {
                "name": f'{model._meta.app_label}.{model.__name__}'
             }
            
            models_data.append(model_info)
        return models_data
    
    def render_to_response(self, context, **response_kwargs):
        html_content = open(f'{pathlib.Path(__file__).parent.resolve()}/templates/django_template_viewer/main.html', 'r').read()
        template = Template(html_content)
        context = Context(context)
        rendered_html = template.render(context)
        return HttpResponse(rendered_html)
    
def save_user_preference(request):
    if request.method == 'GET':
        if 'code_device' in request.GET:
            request.session['code_device'] = request.GET.get('code_device')

        if 'OneToOneField_text' in request.GET:
            request.session['OneToOneField_text'] = request.GET.get('OneToOneField_text')
        if 'OneToOneField_bg' in request.GET:
            request.session['OneToOneField_bg'] = request.GET.get('OneToOneField_bg')

        if 'ForeignKey_text' in request.GET:
            request.session['ForeignKey_text'] = request.GET.get('ForeignKey_text')
        if 'ForeignKey_bg' in request.GET:
            request.session['ForeignKey_bg'] = request.GET.get('ForeignKey_bg')

        if 'ManyToManyField_text' in request.GET:
            request.session['ManyToManyField_text'] = request.GET.get('ManyToManyField_text')
        if 'ManyToManyField_bg' in request.GET:
            request.session['ManyToManyField_bg'] = request.GET.get('ManyToManyField_bg')

        if 'OneToOneRel_text' in request.GET:
            request.session['OneToOneRel_text'] = request.GET.get('OneToOneRel_text')
        if 'OneToOneRel_bg' in request.GET:
            request.session['OneToOneRel_bg'] = request.GET.get('OneToOneRel_bg')

        if 'ManyToOneRel_text' in request.GET:
            request.session['ManyToOneRel_text'] = request.GET.get('ManyToOneRel_text')
        if 'ManyToOneRel_bg' in request.GET:
            request.session['ManyToOneRel_bg'] = request.GET.get('ManyToOneRel_bg')

        if 'ManyToManyRel_text' in request.GET:
            request.session['ManyToManyRel_text'] = request.GET.get('ManyToManyRel_text')
        if 'ManyToManyRel_bg' in request.GET:
            request.session['ManyToManyRel_bg'] = request.GET.get('ManyToManyRel_bg')

        if 'selected_text' in request.GET:
            request.session['selected_text'] = request.GET.get('selected_text')
        if 'selected_bg' in request.GET:
            request.session['selected_bg'] = request.GET.get('selected_bg')

        if 'default_text' in request.GET:
            request.session['default_text'] = request.GET.get('default_text')
        if 'default_bg' in request.GET:
            request.session['default_bg'] = request.GET.get('default_bg')

        if 'method_text' in request.GET:
            request.session['method_text'] = request.GET.get('method_text')
        if 'method_bg' in request.GET:
            request.session['method_bg'] = request.GET.get('method_bg')
        return JsonResponse({'status': 'Preferences saved successfully'})

    return JsonResponse({'status': 'Invalid request method'}, status=400)

def ajax_call(request):
    model = apps.get_model(request.GET.get("model"))

    if not model:
        raise ValueError(f"Error finding model {request.GET.get('model')}")

    field_url = os.path.abspath((apps.get_model(f'{model._meta.app_label}.{model._meta.object_name}').__module__).replace('.', '/') + '.py')
    line_number = inspect.getsourcelines(model)[1]
    
    list_of_parameters_data = inspect.getsourcelines(model)[0]
    list_of_parameters_data.pop(0)
    
    correct_list = []
    for x in list_of_parameters_data:
        cleaned = re.sub(r'\s+', ' ', x.strip())
        correct_list.append(cleaned)
    
    list_of_functions = [method_name for method_name in dir(model) if callable(getattr(model, method_name)) and not method_name.startswith("__") and not method_name == 'DoesNotExist' and not method_name == 'MultipleObjectsReturned' and not method_name.startswith('_')]
    
    correct_list_of_functions = []
    for method_name in list_of_functions:
        method = getattr(model, method_name)  
        try:
            source_code = inspect.getsource(method) 
        except TypeError:
            source_code = "Source code not available"
        
        correct_list_of_functions.append({
            'name': method_name,
            'data': source_code
        })
    
    model_info = {
        "name": f'{model._meta.app_label}.{model.__name__}',
        "fields": {},
        "relations": {"other": [], "set": []},
        "url": {'url': field_url, 'line': line_number},
        "functions": json.dumps(correct_list_of_functions)
    }

    for field in model._meta.get_fields():
        field_type = field.__class__.__name__
        data = None
        
        for x in correct_list:
            if x.startswith(field.name):
                data = x
        field_info = {"name": field.name, "type": field_type, 'data': data or field_type}

        if field_type not in model_info["fields"]:
            model_info["fields"][field_type] = []

        model_info["fields"][field_type].append(field_info)

        if field.is_relation:
            related_model = f'{field.related_model._meta.app_label}.{field.related_model.__name__}' if field.related_model else None
            related_name = getattr(field, "related_name", None) or f"{model.__name__.lower()}_set"
            relation_type = field_type if hasattr(field, "get_internal_type") else "Unknown"

            if not data:
                try:
                    model_for_data = apps.get_model(related_model)
                    model_for_data_list_parameters = inspect.getsourcelines(model_for_data)[0]
                    model_for_data_list_parameters.pop(0)
                    
                    for x in model_for_data_list_parameters:
                        string = re.sub(r'\s+', ' ', x.strip())
                        if string.startswith(field.field.name):
                            data = re.sub(r'\s+', ' ', x.strip())
                            break
                except:
                    data = None
                
                        
            if related_model:
                relation_info = {
                    "related_model": related_model,
                    "related_name": related_name,
                    "field_name": field.name,
                    "relation_type": relation_type,
                    "data": data or related_model
                }
                
                if isinstance(field, (ManyToOneRel, OneToOneRel, ManyToManyRel)):
                    model_info["relations"]["set"].append(relation_info)
                else:
                    model_info["relations"]["other"].append(relation_info)
                    
    return JsonResponse({"data": model_info})

def ajax_call_get_path(request):
    path_json = request.GET.get('list')
    
    if path_json:
        list_of_models = json.loads(path_json)
    else:
        list_of_models = []
        
    model_names = [x.lower() for x in list_of_models]
    correct_list = []
    
    for model_name in model_names:
        correct_list.append(apps.get_model(model_name))
    
    if not correct_list:
        return JsonResponse({'path': ''})
    
    elif len(correct_list) < 2:
        return JsonResponse({'path': str(correct_list[0].__name__)})

    path = f'{correct_list[0].__name__}'

    for i in range(len(correct_list) - 1):
        current_model = correct_list[i]
        next_model = correct_list[i + 1]
        found = False
        
        for field in current_model._meta.get_fields():
            if isinstance(field, (ForeignKey, OneToOneField, ManyToManyField)):
                if field.related_model == next_model:
                    path += f".{field.name}"
                    found = True
                    break
            elif isinstance(field, (ManyToOneRel, OneToOneRel, ManyToManyRel)):
                if field.related_model == next_model:
                    path += f".{field.related_name or next_model.__name__.lower() + '_set'}"
                    found = True
                    break

        if not found:
            path = 'Path not found'
            break

    return JsonResponse({'path': path})


def ajax_call_create_model_create_path(request):
    from_model_name = request.GET.get('model_from')
    to_model_name = request.GET.get('model_to')
    
    if not from_model_name or not to_model_name:
        return JsonResponse({'path': 'Invalid model names'})

    try:
        from_model = apps.get_model(from_model_name)
        to_model = apps.get_model(to_model_name)
    except LookupError:
        return JsonResponse({'path': 'Model not found'})
    
    if from_model == to_model:
        return JsonResponse({'path': f'{from_model.__name__}'})
    
    path = search_path(from_model, to_model)
    return JsonResponse({'path': path or 'Path not found'})

def search_path(current_model, target_model, path=None, visited=None):
    if path is None:
        path = []
    if visited is None:
        visited = set()

    if current_model in visited:
        return None

    visited.add(current_model)

    for field in current_model._meta.get_fields():
        if isinstance(field, (ForeignKey, OneToOneField, ManyToManyField)):
            if field.related_model == target_model:
                return f'{field.name}'

    for field in current_model._meta.get_fields():
        if isinstance(field, (ManyToOneRel, OneToOneRel, ManyToManyRel)):
            if field.related_model == target_model:
                related_name = field.related_name or f"{target_model.__name__.lower()}_set"
                return related_name

    for field in current_model._meta.get_fields():
        if isinstance(field, (ForeignKey, OneToOneField, ManyToManyField)):
            next_model = field.related_model
            if next_model and next_model != current_model:
                sub_path = search_path(next_model, target_model, path, visited)
                if sub_path:
                    return f'{field.name}.{sub_path}'

    for field in current_model._meta.get_fields():
        if isinstance(field, (ManyToOneRel, OneToOneRel, ManyToManyRel)):
            next_model = field.related_model
            if next_model and next_model != current_model:
                related_name = field.related_name or f"{target_model.__name__.lower()}_set"
                sub_path = search_path(next_model, target_model, path, visited)
                if sub_path:
                    return f'{related_name}.{sub_path}'

    return None   
