from fabric.api import hide, lcd, local, settings, task
import fabric.colors as colors

import os
import os.path
import random
import sys
SAFECHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'


def slugify(value):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return mark_safe(re.sub('[-\s]+', '-', value))


@task
def book_project(name, root="~/Documents",
                 template="~/templates/sphinx_project", slug=None):
    """Create a Sphinx documentation project directory."""
    if not slug:
        slug = slugify(name)
    project_dir = _path(root, slug)
    try:
        os.makedirs(project_dir)
    except OSError:  # already exists
        pass
    template_dir = _path(template)
    _copy_template(template_dir, project_dir, name)


@task
def django_env(name, *packages):
    """Bootstrap a python virtualenv and a new Django project"""
    project_name = name
    envdir = _path(os.environ['WORKON_HOME'], project_name)
    with settings(hide('warnings', 'running'), warn_only=True):
        print(colors.blue("Creating virtualenv %s..." % project_name,
                          bold=True))
        local('source /usr/local/bin/virtualenvwrapper.sh;' +
              'mkvirtualenv --no-site-packages %s' % project_name)

        # Bootstrap the django code
        django_project(project_name, envdir)
        project_dir = _path(envdir, project_name)

        local('echo "export DJANGO_SETTINGS_MODULE=' +
              '%s.settingsdev" >>%s/bin/postactivate' % (project_name, envdir))
        local('echo "unset DJANGO_SETTINGS_MODULE" >>' +
              '%s/bin/postdeactivate' % envdir)

        print(colors.blue("Installing pip requirements (may take a while)...",
                          bold=True))
        with lcd(project_dir):
            local('source ../bin/activate; ' +
                  'pip install -r requirements-dev.txt')


@task
def django_project(name, root='.', template='~/templates/django_project'):
    """Create a new Django project (replaces startproject)"""
    project_template = _path(template)
    root_dir = _path(root, name)

    try:
        os.makedirs(root_dir)
    except OSError:  # already exists
        pass

    print colors.blue("Creating Django project %s..." % name, bold=True)
    _copy_template(project_template, root_dir, name)


# Start new Django project
@task
def django_app(name, root='.', template='~/templates/django_app'):
    """Create a new standalone Django app (replaces startapp)"""
    root_dir = _path(root, name)
    template_dir = _path(template)

    try:
        os.makedirs(root_dir)
    except OSError:  # already exists
        pass

    print(colors.blue("Creating Django app %s..." % name, bold=True))
    _copy_template(template_dir, root_dir, name)


# Start new Python project
@task
def pyproject(name, root='.', template='~/templates/pyproject'):
    """Create a new Python project (module or application)"""
    root_dir = _path(root, name)
    template_dir = _path(template)

    try:
        os.makedirs(root_dir)
    except OSError:  # already exists
        pass

    print colors.blue("Creating Python project %s..." % name, bold=True)
    _copy_template(template_dir, root_dir, name)


@task
def test_colors():
    """Prints some strings with color output"""
    print(colors.red("red text"))
    print(colors.red("Bold red text", bold=True))
    print(colors.green("green text"))
    print(colors.green("Bold green text", bold=True))
    print(colors.blue("blue text"))
    print(colors.blue("Bold blue text", bold=True))
    print(colors.cyan("cyan text"))
    print(colors.cyan("Bold cyan text", bold=True))
    print(colors.yellow("yellow text"))
    print(colors.yellow("Bold yellow text", bold=True))
    print(colors.magenta("magenta text"))
    print(colors.magenta("Bold magenta text", bold=True))
    print(colors.white("white text"))
    print(colors.white("Bold white text", bold=True))


################################################
# Utility Functions
################################################
def _path(*args):
    return os.path.realpath(os.path.expanduser(os.path.expandvars(
        os.path.join(*args))))


def _make_writeable(filename):
    """
    Make sure that the file is writeable. Useful if our source is
    read-only.
    """
    import stat
    if sys.platform.startswith('java'):
        # On Jython there is no os.access()
        return
    if not os.access(filename, os.W_OK):
        st = os.stat(filename)
        new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
        os.chmod(filename, new_permissions)


# Lifted from django-extensions and modified slightly -VV
def _copy_template(template_dir, copy_to, project_name, target=None,
                   secret_key=None):
    """copies the specified template directory to the copy_to location"""
    import shutil

    if secret_key is None:
        secret_key = ''.join([random.choice(SAFECHARS) for i in range(52)])

    if target is None:
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
                sys.stderr.write("Notice: Couldn't set permission bits on %s."
                                 % path_new)
                sys.stderr.write("You're probably using an uncommon " +
                                 "filesystem setup. No problem.\n")

