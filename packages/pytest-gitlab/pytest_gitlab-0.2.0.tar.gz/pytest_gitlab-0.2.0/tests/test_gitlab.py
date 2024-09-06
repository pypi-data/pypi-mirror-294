import os

import gitlab


def test_hello_gitlab(gl):
    project = gl.projects.create(name='my-project')
    assert project.name == 'my-project'


def test_create_project(project):
    assert project.name


def test_docker_project_name(docker_compose_project_name):
    assert docker_compose_project_name == 'pytest-python-gitlab'


def test_correct_version(gl):
    if os.environ.get('GITLAB_TAG'):
        if os.environ['GITLAB_TAG'] == 'latest':
            gitlab_gl = gitlab.Gitlab()
            all_gl_tags = [
                x.name
                for x in gitlab_gl.projects.get('gitlab-org/gitlab').tags.list()
                if x.name.startswith('v') and 'rc' not in x.name
            ]
            sorted_gl_tags = sorted(all_gl_tags, reverse=True)
            assert gl.version()[0] == sorted_gl_tags[0][1:]
        else:
            assert gl.version()[0] == os.environ['GITLAB_TAG'][:-2]
