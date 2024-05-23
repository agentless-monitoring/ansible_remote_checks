Name:           ansible_remote_checks
Version:        0.1.4
Release:        0%{?dist}
Summary:        Nagios checks running remotely by Ansible

License:        MIT
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires: python3.11-devel
BuildRequires: python3.11-setuptools
BuildRequires: python3.11-rpm-macros
Requires:       ansible

%description
Nagios checks running remotely by Ansible

%package -n nagios-plugins-ansible-remote
Summary: Nagios checks ansible
Requires: nagios-common
Requires: %{name} = %{version}-%{release}

%description -n nagios-plugins-ansible-remote
Nagios checks ansible

%prep
%autosetup -n %{name}-%{version}

%build
%py3_build

%install
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT --install-scripts %{_libdir}/nagios/plugins

%files
%{python3_sitelib}/*

%files -n nagios-plugins-ansible-remote
%{_libdir}/nagios/plugins/*

%changelog
