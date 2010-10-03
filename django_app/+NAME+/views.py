"""Views for {{ project_name }}"""

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _

def _to_response(request, template, dictionary,):
    """shortcut that calls render_to_response with a RequestContext"""
    return render_to_response(template, dictionary,
        context_instance=RequestContext(request))

# Create your views here.
