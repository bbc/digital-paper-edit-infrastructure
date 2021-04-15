%global __os_install_post %{nil}
Name: digital-paper-edit-client
AutoReqProv: no
Version: 1.0.0%{?buildnum:.%{buildnum}}
Release: 1%{?dist}
Group: System Environment/Daemons
License: Internal BBC use only
Summary: %{name}
Source0: %{name}.tar.gz
BuildArch: noarch

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Cert termination
Requires: nodejs
# Requires: partner-platform-access-proxy
Requires: cloud-httpd24-ssl-services-devs-staff

# amazon cloudwatch agent
# Requires: amazon-cloudwatch-agent

# For debugging purposes
Requires: net-tools
Requires: vim

%description
${name}

%prep
%setup -q -n src

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}/lib/%{name}
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/
mkdir -p %{buildroot}%{_sysconfdir}/bake-scripts
mkdir -p %{buildroot}%{_sysconfdir}/%{name}

cp -r usr/lib/%{name}/* %{buildroot}%{_prefix}/lib/%{name}
cp -r usr/lib/systemd/* %{buildroot}%{_prefix}/lib/systemd
cp -r etc/* %{buildroot}%{_sysconfdir}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -d / -s /sbin/nologin %{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun

%files
%defattr(-, root, root, 0755)
%{_sysconfdir}/bake-scripts/*

%defattr(644, root, root, 755)
%{_prefix}/lib/systemd/system/*
%{_prefix}/lib/%{name}/*