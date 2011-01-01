import os
import os.path

import random
from fabric.api import *

def django_env(project_name, *packages):
    """Bootstrap a python virtualenv and a new Django project"""
    
    envdir = _path(os.environ['WORKON_HOME'], project_name)
    with settings(hide('warnings', 'running'), warn_only=True):
        print "Creating virtualenv %s..." % project_name
        local('source /usr/local/bin/virtualenvwrapper.sh; mkvirtualenv --no-site-packages %s' % project_name)

        # Bootstrap the django code
        django_project(project_name, envdir)
        project_dir = _path(envdir, project_name)

        local('echo "export DJANGO_SETTINGS_MODULE=%s.settingsdev" >> %s/bin/postactivate'% (project_name, envdir))
        local('echo "unset DJANGO_SETTINGS_MODULE" >> %s/bin/postdeactivate'% envdir)

        print "Install pip requirements (may take a while)..."
        with cd(project_dir):
            local('source ../bin/activate; pip install -r requirements-dev.txt')


def django_project(name, root='.', template='~/templates/django_project'):
    """Create a new Django project (replaces startproject)"""
    project_template = _path(template)
    root_dir = _path(root, name)

    try:
        os.makedirs(root_dir)
    except OSError: # already exists
        pass

    print "Creating Django project %s..." % name
    _copy_template(project_template, root_dir, name)


# Start new Django project
def django_app(name, root='.', template='~/templates/django_app'):
    """Create a new standalone Django app (replaces startapp)"""
    root_dir = _path(root, name)
    template_dir = _path(template)

    try:
        os.makedirs(root_dir)
    except OSError: # already exists
        pass

    print "Creating Django app %s..." % name
    _copy_template(template_dir, root_dir, name)


################################################
# Utility Functions
################################################
def _path(*args):
    return os.path.realpath(os.path.expanduser(os.path.expandvars(os.path.join(*args))))


# Lifted from django-extensions and modified slightly -VV
def _copy_template(template_dir, copy_to, project_name, target=None, 
    secret_key = ''.join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(52)])):
    """copies the specified template directory to the copy_to location"""
    import shutil
    from django.core.management.base import _make_writeable
    
    if target == None: 
        target = project_name

    template_dir = os.path.normpath(template_dir)
    # walks the template structure and copies it
    for d, subdirs, files in os.walk(template_dir):
        relative_dir = d[len(template_dir)+1:]
        d_new = os.path.join(copy_to, relative_dir).replace('+NAME+', target)
        if relative_dir and not os.path.exists(d_new):
            os.mkdir(d_new)
        for i, subdir in enumerate(subdirs):
            if subdir.startswith('.'):
                del subdirs[i]
        for f in files:
            if f.endswith('.pyc') or f.startswith('.DS_Store'):
                continue
            path_old = os.path.join(d, f)
            path_new = os.path.join(d_new, f.replace('+NAME+', target))
            if os.path.exists(path_new):
                path_new = os.path.join(d_new, f)
                if os.path.exists(path_new):
                    continue
            if path_new.endswith('.tmpl'):
                path_new = path_new[:-5]
            fp_old = open(path_old, 'r')
            fp_new = open(path_new, 'w')
            fp_new.write(fp_old.read()
                .replace('{{ project_name }}', project_name)
                .replace('{{ secret_key }}', secret_key)
            )
            fp_old.close()
            fp_new.close()
            try:
                shutil.copymode(path_old, path_new)
                _make_writeable(path_new)
            except OSError:
                sys.stderr.write("Notice: Couldn't set permission bits on %s. You're probably using an uncommon filesystem setup. No problem.\n" % path_new)


