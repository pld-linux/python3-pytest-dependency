#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Manage dependencies of tests
Summary(pl.UTF-8):	Zarządzanie zależnościami testów
Name:		python3-pytest-dependency
Version:	0.6.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-dependency/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-dependency/pytest-dependency-%{version}.tar.gz
# Source0-md5:	a4c76010afb7adaf07be18bb709bacd0
URL:		https://pypi.org/project/pytest-dependency/
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest >= 3.7.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.4
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

%prep
%setup -q -n pytest-dependency-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_dependency \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p doc/examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%{py3_sitescriptdir}/pytest_dependency.py
%{py3_sitescriptdir}/__pycache__/pytest_dependency.cpython-*.py[co]
%{py3_sitescriptdir}/pytest_dependency-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}
