%define name digital-paper-edit-infrastructure
%define version 1.0.0
%define release 0
%define buildroot %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Name: %{name}
Version: %{version}
Release: %{release}
Summary: digital-paper-edit-infrastructure

Group: Installation Script
License: ISC
Source: %{name}.tar.gz
BuildRoot: %{buildroot}
Requires: nodejs
Requires: cloud-httpd24-ssl-no-certs
Requires: api-management
BuildRequires: nodejs
AutoReqProv: no

%description
digital-paper-edit-infrastructure

%prep
%setup -q -c -n %{name}

%build
npm prune --production
npm rebuild

%pre
getent group digital-paper-edit-infrastructur >/dev/null || groupadd -r digital-paper-edit-infrastructur
getent passwd digital-paper-edit-infrastructur >/dev/null || useradd -r -g digital-paper-edit-infrastructur -G digital-paper-edit-infrastructur -d / -s /sbin/nologin -c "digital-paper-edit-infrastructur" digital-paper-edit-infrastructur

%install
mkdir -p %{buildroot}/usr/lib/digital-paper-edit-infrastructure
cp -r ./ %{buildroot}/usr/lib/digital-paper-edit-infrastructure
mkdir -p %{buildroot}/var/log/digital-paper-edit-infrastructure

%post
systemctl enable /usr/lib/digital-paper-edit-infrastructure/digital-paper-edit-infrastructure.service
mkdir -p /etc/bake-scripts/digital-paper-edit-infrastructure
cp -rf /usr/lib/digital-paper-edit-infrastructure/bake-scripts/* /etc/bake-scripts/digital-paper-edit-infrastructure/
./scripts/create-service-config.sh

%clean
rm -rf %{buildroot}

%files
%defattr(644, digital-paper-edit-infrastructur, digital-paper-edit-infrastructur, 755)
/usr/lib/digital-paper-edit-infrastructure
/var/log/digital-paper-edit-infrastructure
%attr(755, digital-paper-edit-infrastructur, digital-paper-edit-infrastructur) /usr/lib/digital-paper-edit-infrastructure/bake-scripts/*
