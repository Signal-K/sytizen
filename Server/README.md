# Containerisation for local development

In this folder, `Dockerfile` runs the Flask Server in a container.

For convenience, a Makefile supports the following simple operations:

* `make build` builds an image from the current working copy
* `make run` starts this image in a container

## Prerequisites

You will need to have a Docker environment available... Docker Desktop or an equivalent

## Previous Issue

The build step (`make build`) fails whilst running `pipenv install` during the build of the Docker image.

`thirdweb-sdk` caused errors on `pipenv install`. The output was long and ugly; no resolution has been found, so we are removing this for now.

## Current Issue

`pipenv install` is reporting an error during `make build`:

```
 > [6/6] RUN pipenv install:                                                                                                                                                                                                                                                                   
#10 0.446 Creating a virtualenv for this project...                                                                                                                                                                                                                                            
#10 0.446 Pipfile: /app/Pipfile                                                                                                                                                                                                                                                                
#10 0.456 Using /usr/local/bin/python (3.9.9) to create virtualenv...                                                                                                                                                                                                                          
#10 0.781 created virtual environment CPython3.9.9.final.0-64 in 239ms                                                                                                                                                                                                                         
#10 0.781   creator CPython3Posix(dest=/root/.local/share/virtualenvs/app-4PlAip0Q, clear=False, no_vcs_ignore=False, global=False)
#10 0.781   seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/root/.local/share/virtualenv)
#10 0.781     added seed packages: pip==22.3.1, setuptools==65.6.3, wheel==0.38.4
#10 0.781   activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator
#10 0.781 
#10 0.783 ✔ Successfully created virtual environment!
#10 0.838 Virtualenv location: /root/.local/share/virtualenvs/app-4PlAip0Q
#10 0.845 Pipfile.lock (27d268) out of date, updating to (cb9ab7)...
#10 0.846 Locking [packages] dependencies...
#10 3.900 
#10 3.900 ERROR:pip.subprocessor:[present-rich] python setup.py egg_info exited with 1
#10 3.900 [ResolutionFailure]:   File "/usr/local/lib/python3.9/site-packages/pipenv/resolver.py", line 811, in _main
#10 3.900 [ResolutionFailure]:       resolve_packages(
#10 3.900 [ResolutionFailure]:   File "/usr/local/lib/python3.9/site-packages/pipenv/resolver.py", line 759, in resolve_packages
#10 3.900 [ResolutionFailure]:       results, resolver = resolve(
#10 3.900 [ResolutionFailure]:   File "/usr/local/lib/python3.9/site-packages/pipenv/resolver.py", line 738, in resolve
#10 3.900 [ResolutionFailure]:       return resolve_deps(
#10 3.900 [ResolutionFailure]:   File "/usr/local/lib/python3.9/site-packages/pipenv/utils/resolver.py", line 1100, in resolve_deps
#10 3.900 [ResolutionFailure]:       results, hashes, markers_lookup, resolver, skipped = actually_resolve_deps(
#10 3.900 [ResolutionFailure]:   File "/usr/local/lib/python3.9/site-packages/pipenv/utils/resolver.py", line 899, in actually_resolve_deps
#10 3.900 [ResolutionFailure]:       resolver.resolve()
#10 3.900 [ResolutionFailure]:   File "/usr/local/lib/python3.9/site-packages/pipenv/utils/resolver.py", line 687, in resolve
#10 3.900 [ResolutionFailure]:       raise ResolutionFailure(message=str(e))
#10 3.900 [pipenv.exceptions.ResolutionFailure]: Warning: Your dependencies could not be resolved. You likely have a mismatch in your sub-dependencies.
#10 3.900   You can use $ pipenv install --skip-lock to bypass this mechanism, then run $ pipenv graph to inspect the situation.
#10 3.900   Hint: try $ pipenv lock --pre if it is a pre-release dependency.
#10 3.900 ERROR: metadata generation failed
#10 3.900 
------
```

Using the suggested `--skip-lock` provides more detail:

The key is:
```
#10 3.311 [pipenv.exceptions.InstallError]:       Error: pg_config executable not found.
#10 3.311 [pipenv.exceptions.InstallError]:       
#10 3.311 [pipenv.exceptions.InstallError]:       pg_config is required to build psycopg2 from source.  Please add the directory
#10 3.312 [pipenv.exceptions.InstallError]:       containing pg_config to the $PATH or specify the full executable path with the
#10 3.312 [pipenv.exceptions.InstallError]:       option:
```

For reference, the full error is below.

Since we are currently specifying both `psycopg2` and `psycopg2-binary`, I'll remove the first one.


```
(Server) sytizen/Server server-docker % make build     
docker build --tag sytizen-server .
[+] Building 6.0s (10/11)                                                                                                                                                                                                                                                                      
 => [internal] load build definition from Dockerfile                                                                                                                                                                                                                                      0.0s
 => => transferring dockerfile: 391B                                                                                                                                                                                                                                                      0.0s
 => [internal] load .dockerignore                                                                                                                                                                                                                                                         0.0s
 => => transferring context: 2B                                                                                                                                                                                                                                                           0.0s
 => [internal] load metadata for docker.io/library/python:3.9.9-slim-bullseye                                                                                                                                                                                                             2.3s
 => [1/7] FROM docker.io/library/python:3.9.9-slim-bullseye@sha256:f4efbe5d1eb52c221fded79ddf18e4baa0606e7766afe2f07b0b330a9e79564a                                                                                                                                                       0.0s
 => [internal] load build context                                                                                                                                                                                                                                                         0.0s
 => => transferring context: 6.16kB                                                                                                                                                                                                                                                       0.0s
 => CACHED [2/7] WORKDIR /app                                                                                                                                                                                                                                                             0.0s
 => CACHED [3/7] RUN pip install pipenv                                                                                                                                                                                                                                                   0.0s
 => CACHED [4/7] WORKDIR /app                                                                                                                                                                                                                                                             0.0s
 => [5/7] COPY . .                                                                                                                                                                                                                                                                        0.0s
 => ERROR [6/7] RUN pipenv install --skip-lock                                                                                                                                                                                                                                            3.5s
------                                                                                                                                                                                                                                                                                         
 > [6/7] RUN pipenv install --skip-lock:                                                                                                                                                                                                                                                       
#10 0.614 Creating a virtualenv for this project...                                                                                                                                                                                                                                            
#10 0.614 Pipfile: /app/Pipfile                                                                                                                                                                                                                                                                
#10 0.625 Using /usr/local/bin/python (3.9.9) to create virtualenv...                                                                                                                                                                                                                          
#10 1.068 created virtual environment CPython3.9.9.final.0-64 in 334ms                                                                                                                                                                                                                         
#10 1.068   creator CPython3Posix(dest=/root/.local/share/virtualenvs/app-4PlAip0Q, clear=False, no_vcs_ignore=False, global=False)
#10 1.068   seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/root/.local/share/virtualenv)
#10 1.068     added seed packages: pip==22.3.1, setuptools==65.6.3, wheel==0.38.4
#10 1.068   activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator
#10 1.068 
#10 1.071 ✔ Successfully created virtual environment!
#10 1.126 Virtualenv location: /root/.local/share/virtualenvs/app-4PlAip0Q
#10 1.127 Installing dependencies from Pipfile...
#10 2.479 An error occurred while installing moralis! Will try again.
#10 2.479 An error occurred while installing flask! Will try again.
#10 2.479 An error occurred while installing flask-cors! Will try again.
#10 2.480 An error occurred while installing python-dotenv! Will try again.
#10 2.480 An error occurred while installing psycopg2! Will try again.
#10 2.480 An error occurred while installing matplotlib! Will try again.
#10 2.480 An error occurred while installing lightkurve! Will try again.
#10 2.481 An error occurred while installing nbformat! Will try again.
#10 2.481 An error occurred while installing gunicorn! Will try again.
#10 2.481 An error occurred while installing sqlalchemy! Will try again.
#10 2.481 An error occurred while installing psycopg2-binary! Will try again.
#10 2.482 An error occurred while installing flask-sqlalchemy! Will try again.
#10 2.482 Installing initially failed dependencies...
#10 3.309 [pipenv.exceptions.InstallError]: Collecting moralis
#10 3.309 [pipenv.exceptions.InstallError]:   Using cached moralis-0.1.19-py3-none-any.whl (665 kB)
#10 3.309 [pipenv.exceptions.InstallError]: Collecting flask
#10 3.309 [pipenv.exceptions.InstallError]:   Using cached Flask-2.2.2-py3-none-any.whl (101 kB)
#10 3.310 [pipenv.exceptions.InstallError]: Collecting flask-cors
#10 3.310 [pipenv.exceptions.InstallError]:   Using cached Flask_Cors-3.0.10-py2.py3-none-any.whl (14 kB)
#10 3.310 [pipenv.exceptions.InstallError]: Collecting python-dotenv
#10 3.310 [pipenv.exceptions.InstallError]:   Using cached python_dotenv-0.21.1-py3-none-any.whl (19 kB)
#10 3.310 [pipenv.exceptions.InstallError]: Collecting psycopg2
#10 3.310 [pipenv.exceptions.InstallError]:   Using cached psycopg2-2.9.5.tar.gz (384 kB)
#10 3.310 [pipenv.exceptions.InstallError]:   Preparing metadata (setup.py): started
#10 3.310 [pipenv.exceptions.InstallError]:   Preparing metadata (setup.py): finished with status 'error'
#10 3.310 [pipenv.exceptions.InstallError]: error: subprocess-exited-with-error
#10 3.310 [pipenv.exceptions.InstallError]:   
#10 3.310 [pipenv.exceptions.InstallError]:   × python setup.py egg_info did not run successfully.
#10 3.310 [pipenv.exceptions.InstallError]:   │ exit code: 1
#10 3.310 [pipenv.exceptions.InstallError]:   ╰─> [25 lines of output]
#10 3.311 [pipenv.exceptions.InstallError]:       /root/.local/share/virtualenvs/app-4PlAip0Q/lib/python3.9/site-packages/setuptools/config/setupcfg.py:508: SetuptoolsDeprecationWarning: The license_file parameter is deprecated, use license_files instead.
#10 3.311 [pipenv.exceptions.InstallError]:         warnings.warn(msg, warning_class)
#10 3.311 [pipenv.exceptions.InstallError]:       running egg_info
#10 3.311 [pipenv.exceptions.InstallError]:       creating /tmp/pip-pip-egg-info-7o8c0k__/psycopg2.egg-info
#10 3.311 [pipenv.exceptions.InstallError]:       writing /tmp/pip-pip-egg-info-7o8c0k__/psycopg2.egg-info/PKG-INFO
#10 3.311 [pipenv.exceptions.InstallError]:       writing dependency_links to /tmp/pip-pip-egg-info-7o8c0k__/psycopg2.egg-info/dependency_links.txt
#10 3.311 [pipenv.exceptions.InstallError]:       writing top-level names to /tmp/pip-pip-egg-info-7o8c0k__/psycopg2.egg-info/top_level.txt
#10 3.311 [pipenv.exceptions.InstallError]:       writing manifest file '/tmp/pip-pip-egg-info-7o8c0k__/psycopg2.egg-info/SOURCES.txt'
#10 3.311 [pipenv.exceptions.InstallError]:       
#10 3.311 [pipenv.exceptions.InstallError]:       Error: pg_config executable not found.
#10 3.311 [pipenv.exceptions.InstallError]:       
#10 3.311 [pipenv.exceptions.InstallError]:       pg_config is required to build psycopg2 from source.  Please add the directory
#10 3.312 [pipenv.exceptions.InstallError]:       containing pg_config to the $PATH or specify the full executable path with the
#10 3.312 [pipenv.exceptions.InstallError]:       option:
#10 3.312 [pipenv.exceptions.InstallError]:       
#10 3.312 [pipenv.exceptions.InstallError]:           python setup.py build_ext --pg-config /path/to/pg_config build ...
#10 3.312 [pipenv.exceptions.InstallError]:       
#10 3.312 [pipenv.exceptions.InstallError]:       or with the pg_config option in 'setup.cfg'.
#10 3.312 [pipenv.exceptions.InstallError]:       
#10 3.312 [pipenv.exceptions.InstallError]:       If you prefer to avoid building psycopg2 from source, please install the PyPI
#10 3.312 [pipenv.exceptions.InstallError]:       'psycopg2-binary' package instead.
#10 3.312 [pipenv.exceptions.InstallError]:       
#10 3.312 [pipenv.exceptions.InstallError]:       For further information please check the 'doc/src/install.rst' file (also at
#10 3.313 [pipenv.exceptions.InstallError]:       <https://www.psycopg.org/docs/install.html>).
#10 3.313 [pipenv.exceptions.InstallError]:       
#10 3.313 [pipenv.exceptions.InstallError]:       [end of output]
#10 3.313 [pipenv.exceptions.InstallError]:   
#10 3.313 [pipenv.exceptions.InstallError]:   note: This error originates from a subprocess, and is likely not a problem with pip.
#10 3.313 [pipenv.exceptions.InstallError]: error: metadata-generation-failed
#10 3.313 [pipenv.exceptions.InstallError]: 
#10 3.313 [pipenv.exceptions.InstallError]: × Encountered error while generating package metadata.
#10 3.313 [pipenv.exceptions.InstallError]: ╰─> See above for output.
#10 3.313 [pipenv.exceptions.InstallError]: 
#10 3.313 [pipenv.exceptions.InstallError]: note: This is an issue with the package mentioned above, not pip.
#10 3.314 [pipenv.exceptions.InstallError]: hint: See above for details.
#10 3.314 ERROR: Couldn't install package: [Requirement(_name='moralis', vcs=None, req=NamedRequirement(name='moralis', version='', req=Requirement.parse('moralis'), extras=[], editable=False, _parsed_line=<Line (editable=False, name=moralis, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=moralis)>), markers=None, _specifiers='', index=None, editable=False, hashes=frozenset(), extras=(), abstract_dep=None, _line_instance=<Line (editable=False, name=moralis, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=moralis)>, _ireq=None), Requirement(_name='flask', vcs=None, req=NamedRequirement(name='flask', version='', req=Requirement.parse('flask'), extras=[], editable=False, _parsed_line=<Line (editable=False, name=flask, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=flask)>), markers=None, _specifiers='', index=None, editable=False, hashes=frozenset(), extras=(), abstract_dep=None, _line_instance=<Line (editable=False, name=flask, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=flask)>, _ireq=None), Requirement(_name='flask-cors', vcs=None, req=NamedRequirement(name='flask-cors', version='', req=Requirement.parse('flask-cors'), extras=[], editable=False, _parsed_line=<Line (editable=False, name=flask-cors, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=flask-cors)>), markers=None, _specifiers='', index=None, editable=False, hashes=frozenset(), extras=(), abstract_dep=None, _line_instance=<Line (editable=False, name=flask-cors, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=flask-cors)>, _ireq=None), Requirement(_name='python-dotenv', vcs=None, req=NamedRequirement(name='python-dotenv', version='', req=Requirement.parse('python-dotenv'), extras=[], editable=False, _parsed_line=<Line (editable=False, name=python-dotenv, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=python-dotenv)>), markers=None, _specifiers='', index=None, editable=False, hashes=frozenset(), extras=(), abstract_dep=None, _line_instance=<Line (editable=False, name=python-dotenv, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=python-dotenv)>, _ireq=None), Requirement(_name='psycopg2', vcs=None, req=NamedRequirement(name='psycopg2', version='', req=Requirement.parse('psycopg2'), extras=[], editable=False, _parsed_line=<Line (editable=False, name=psycopg2, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=psycopg2)>), markers=None, _specifiers='', index=None, editable=False, hashes=frozenset(), extras=(), abstract_dep=None, _line_instance=<Line (editable=False, name=psycopg2, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=psycopg2)>, _ireq=None), Requirement(_name='matplotlib', vcs=None, req=NamedRequirement(name='matplotlib', version='', req=Requirement.parse('matplotlib'), extras=[], editable=False, _parsed_line=<Line (editable=False, name=matplotlib, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=matplotlib)>), markers=None, _specifiers='', index=None, editable=False, hashes=frozenset(), extras=(), abstract_dep=None, _line_instance=<Line (editable=False, name=matplotlib, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=matplotlib)>, _ireq=None), Requirement(_name='lightkurve', vcs=None, req=NamedRequirement(name='lightkurve', version='', req=Requirement.parse('lightkurve'), extras=[], editable=False, _parsed_line=<Line (editable=False, name=lightkurve, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=lightkurve)>), markers=None, _specifiers='', index=None, editable=False, hashes=frozenset(), extras=(), abstract_dep=None, _line_instance=<Line (editable=False, name=lightkurve, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=lightkurve)>, _ireq=None), Requirement(_name='nbformat', vcs=None, req=NamedRequirement(name='nbformat', version='', req=Requirement.parse('nbformat'), extras=[], editable=False, _parsed_line=<Line (editable=False, name=nbformat, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=nbformat)>), markers=None, _specifiers='', index=None, editable=False, hashes=frozenset(), extras=(), abstract_dep=None, _line_instance=<Line (editable=False, name=nbformat, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=nbformat)>, _ireq=None), Requirement(_name='gunicorn', vcs=None, req=NamedRequirement(name='gunicorn', version='', req=Requirement.parse('gunicorn'), extras=[], editable=False, _parsed_line=<Line (editable=False, name=gunicorn, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=gunicorn)>), markers=None, _specifiers='', index=None, editable=False, hashes=frozenset(), extras=(), abstract_dep=None, _line_instance=<Line (editable=False, name=gunicorn, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=gunicorn)>, _ireq=None), Requirement(_name='sqlalchemy', vcs=None, req=NamedRequirement(name='sqlalchemy', version='', req=Requirement.parse('sqlalchemy'), extras=[], editable=False, _parsed_line=<Line (editable=False, name=sqlalchemy, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=sqlalchemy)>), markers=None, _specifiers='', index=None, editable=False, hashes=frozenset(), extras=(), abstract_dep=None, _line_instance=<Line (editable=False, name=sqlalchemy, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=sqlalchemy)>, _ireq=None), Requirement(_name='psycopg2-binary', vcs=None, req=NamedRequirement(name='psycopg2-binary', version='', req=Requirement.parse('psycopg2-binary'), extras=[], editable=False, _parsed_line=<Line (editable=False, name=psycopg2-binary, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=psycopg2-binary)>), markers=None, _specifiers='', index=None, editable=False, hashes=frozenset(), extras=(), abstract_dep=None, _line_instance=<Line (editable=False, name=psycopg2-binary, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=psycopg2-binary)>, _ireq=None), Requirement(_name='flask-sqlalchemy', vcs=None, req=NamedRequirement(name='flask-sqlalchemy', version='', req=Requirement.parse('flask-sqlalchemy'), extras=[], editable=False, _parsed_line=<Line (editable=False, name=flask-sqlalchemy, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=flask-sqlalchemy)>), markers=None, _specifiers='', index=None, editable=False, hashes=frozenset(), extras=(), abstract_dep=None, _line_instance=<Line (editable=False, name=flask-sqlalchemy, path=None, uri=None, extras=(), markers=None, vcs=None, specifier=None, pyproject=None, pyproject_requires=None, pyproject_backend=None, ireq=flask-sqlalchemy)>, _ireq=None)]
#10 3.314  Package installation failed...
------
executor failed running [/bin/sh -c pipenv install --skip-lock]: exit code: 1
make: *** [build] Error 1
```