%global modname ansible-remote-checks
%if %{?rhel} == 8
%define python_version python3
%endif
%if %{?rhel} == 9
%define python_version python3.11
%endif
Name:           %{python_version}-%{modname}
Version:        0.1.4
Release:        2%{?dist}
Summary:        Nagios checks for linux hosts executed agentless via ansible

License:        MIT
Source0:        %{modname}-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: %{python_version}-devel
BuildRequires: %{python_version}-rpm-macros
BuildRequires: python3-setuptools
Requires:      ansible-core

%?python_disable_dependency_generator

%description
Nagios checks for linux hosts executed agentless via ansible

%package -n nagios-plugins-ansible-remote
Summary: Nagios checks ansible
Requires: nagios-common
Requires: %{name} = %{version}-%{release}

%description -n nagios-plugins-ansible-remote
Nagios checks ansible

%prep
%autosetup -n %{modname}-%{version}

%build
%py3_build

%install
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT --install-scripts %{_libdir}/nagios/plugins

%files
%{python3_sitelib}/*

%files -n nagios-plugins-ansible-remote
%{_libdir}/nagios/plugins/*

%changelog
