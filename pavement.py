import os
from random import choice

from paver.easy import *
import paver.virtual

options(
    virtualenv = Bunch(
        basedir = path(os.environ['WORKON_HOME']),
        no_site_packages = True,
    ),
    django_project = Bunch(
        project_template = '/Users/vince/templates/django_project'
    ),
    django_app = Bunch(
        template = '/Users/vince/templates/django_app'
    )
)

@task
def saywhat(options):
    """Just print some variables"""
    print repr(options)


@task
@consume_args
def django_env(options, args):
    """Create a new python virtualenv to start a new Django project"""

    if len(args) > 0:
        project_name = args[0]
        packages = args[1:]
    else:
        project_name = options.project_name
        
    envdir = options.basedir / project_name

    # Set up options for virtualenv
    options.virtualenv['dest_dir'] = envdir
    options.virtualenv['packages_to_install'] = [
        'coverage',
        'docutils>=0.3',
        'django>=1.2,<1.3',
        'django-debug-toolbar',
        'django-extensions',
        'django-staticfiles',
        'PIL', # required for ImageField
        # 'pylint',
        'python-dateutil',
        'python-memcached',
        'pytz',
        'south>0.7',
    ]
    
    # consider additional command line args to be packages to install
    # Temporarily removed while refactoring -VV 2010-10-06
    # if len(args) > 1:
    #     options.virtualenv['packages_to_install'].extend(args[1:])

    # initialize a virtualenv
    # os.mkdir(envdir)
    # path.chdir(envdir)
    # call_task('paver.virtual.bootstrap')
    # The bootstrap script doesn't use all the swell virtualenvwrapper hooks. :(
    # sh('python bootstrap.py')
    sh('source /usr/local/bin/virtualenvwrapper.sh; mkvirtualenv --no-site-packages --distribute %s'%project_name)
    path.chdir(envdir)
    
    # Bootstrap the django code
    options.django_project['name'] = project_name
    options.django_project['root_dir'] = envdir / 'project'
    call_task('django_project')
    sh('echo "export DJANGO_SETTINGS_MODULE=%s.settingsdev" >> ./bin/postactivate'%project_name)
    sh('echo "unset DJANGO_SETTINGS_MODULE" >> ./bin/postdeactivate')
    sh('source bin/activate; cd project; python setup.py develop')
    sh('source bin/activate; pip install -r project/requirements-dev.txt')


@task
@cmdopts([
    ('name=', 'n', 'Project namespace'),
    ('root_dir=', 'd', 'Directory in which to start the project, default=./{name}'),
    ('project_template=', 't', 'Project template')
    ])
def django_project(options):
    """Create a new Django project (replaces startproject)"""
    project_name = options.django_project.name
    project_template = options.django_project.project_template
    if options.django_project.get('root_dir'):
        root_dir = path(options.django_project.root_dir).realpath()
    else:
        root_dir = path('./' + options.django_project.name).realpath()

    # Start new Django project
    try:
        root_dir.mkdir()
    except OSError: # already exists
        pass

    copy_template(project_template, root_dir, project_name)


@task
@cmdopts([
    ('name=', 'n', 'Python name for the app'),
    ('root_dir=', 'd', 'Directory in which to start the app, default=./{name}'),
    ('template=', 't', 'App template directory')
    ])
def django_app(options):
    """Create a new standalone (reusable) Django app (replaces startapp)"""
    name = options.django_app.name
    template_dir = options.django_app.template
    if options.django_app.get('root_dir'):
        root_dir = path(options.django_app.root_dir).realpath()
    else:
        root_dir = path('./' + options.django_app.name).realpath()

    # Start new Django project
    try:
        root_dir.mkdir()
    except OSError: # already exists
        pass

    copy_template(template_dir, root_dir, name)


# Lifted from django-extensions and modified slightly -VV
def copy_template(template_dir, copy_to, project_name, target=None, 
    secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(52)])):
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



