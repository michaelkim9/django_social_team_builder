from django import template
from projects.models import Project, Position, Skill

register = template.Library()


@register.inclusion_tag('need_nav.html')
def nav_need_func():
    needs = ['All Needs','Android', 'Designer', 'Java ','PHP','Python',
             'Rails','Wordpress', 'iOS']
    return {'needs': needs}
