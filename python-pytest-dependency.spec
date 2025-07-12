#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (fails with pytest 6+, see python3-pytest-dependency.spec)

Summary:	Manage dependencies of tests
Summary(pl.UTF-8):	Zarządzanie zależnościami testów
Name:		python-pytest-dependency
# keep 0.5.x here for python2 support
Version:	0.5.1
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-dependency/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-dependency/pytest-dependency-%{version}.tar.gz
# Source0-md5:	ed8a84ff2131c191983e64437af5746b
URL:		https://pypi.org/project/pytest-dependency/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm
%if %{with tests}
BuildRequires:	python-pytest >= 3.6.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	python3-pytest >= 3.6.0
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This pytest plugin manages dependencies of tests. It allows to mark
some tests as dependent from other tests. These tests will then be
skipped if any of the dependencies did fail or has been skipped.

%description -l pl.UTF-8
Ta wtyczka pytesta zarządza zależnościami testów. Pozwala oznaczać
niektóre testy jako zależne od innych testów. Testy te będą pomijane,
jeśli dowolna ich zależność się nie powiedzie lub zostanie pominięta.

%package -n python3-pytest-dependency
Summary:	Manage dependencies of tests
Summary(pl.UTF-8):	Zarządzanie zależnościami testów
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-pytest-dependency
This pytest plugin manages dependencies of tests. It allows to mark
some tests as dependent from other tests. These tests will then be
skipped if any of the dependencies did fail or has been skipped.

%description -n python3-pytest-dependency -l pl.UTF-8
Ta wtyczka pytesta zarządza zależnościami testów. Pozwala oznaczać
niektóre testy jako zależne od innych testów. Testy te będą pomijane,
jeśli dowolna ich zależność się nie powiedzie lub zostanie pominięta.

%package apidocs
Summary:	API documentation for Python pytest-dependency module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pytest-dependency
Group:		Documentation

%description apidocs
API documentation for Python pytest-dependency module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pytest-dependency.

%prep
%setup -q -n pytest-dependency-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_dependency \
PYTHONPATH=$(pwd) \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_dependency \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitescriptdir}/pytest_dependency.py[co]
%{py_sitescriptdir}/pytest_dependency-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pytest-dependency
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/pytest_dependency.py
%{py3_sitescriptdir}/__pycache__/pytest_dependency.cpython-*.py[co]
%{py3_sitescriptdir}/pytest_dependency-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/{_static,*.html,*.js}
%endif
