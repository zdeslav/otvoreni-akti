from django.http import JsonResponse
from django.db.models import Q
from .models import Act

base_url = 'http://web.zagreb.hr/'


def search_results_view(request, search_term):
    query_set = Act.objects.filter(
        Q(content__icontains=search_term)
        | Q(subject__icontains=search_term)
    ).distinct()
    result = {'matches': [base_url + m.content_url for m in query_set]}
    return JsonResponse(result)
