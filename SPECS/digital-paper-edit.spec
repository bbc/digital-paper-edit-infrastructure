%define name digital-paper-edit

Name: %{name}
Summary: digital-paper-edit
Version: 0.1.1%{?buildnum:.%{buildnum}}
Release: 1%{?dist}
Group: System Environment/Daemons
License: Internal BBC use only
Summary: Digital Paper Edit Infrastructure
Source0: src.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: x86_64

Requires: nodejs
Requires: cloud-httpd24-ssl-no-certs

BuildRequires: systemd
BuildRequires: nodejs

%description
digital-paper-edit

%prep
%setup -q -n src/

%build
npm prune --production
npm rebuild

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -G %{name} -d / -s /sbin/nologin -c "%{name}" %{name}

%install
mkdir -p %{buildroot}/usr/lib/systemd/system/
mkdir -p %{buildroot}/usr/lib/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/bake-scripts/%{name}
mkdir -p %{buildroot}/var/log/%{name}

cp %{_builddir}/src/server.js %{buildroot}/usr/lib/%{name}
cp %{_builddir}/src/usr/lib/systemd/system/%{name}.service %{buildroot}/usr/lib/systemd/system

cp -R %{_builddir}/src/%{name}/ %{buildroot}/usr/lib/%{name}/
cp -R %{_builddir}/src/node_modules %{buildroot}/usr/lib/%{name}
cp -R %{_builddir}/src/bake-scripts %{buildroot}%{_sysconfdir}/bake-scripts/%{name}


%files
%defattr(644, root, root, 755)
/usr/lib/%{name}
/usr/lib/systemd/system/%{name}.service
/var/log/%{name}
%defattr(-, root, root, 755)
/etc/bake-scripts/%{name}
