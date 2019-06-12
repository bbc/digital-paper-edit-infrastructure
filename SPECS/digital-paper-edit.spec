%define name digital-paper-edit

Name: %{name}
Summary: digital-paper-edit
Version: 0.1.1%{?buildnum:.%{buildnum}}
Release: 1%{?dist}
Group: System Environment/Daemons
License: Internal BBC use only
Summary: Digital Paper Edit Infrastructure
#Source0: src.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: x86_64

Requires: dpe-client = 0.1.1-2
Requires: dpe-api = 0.1.1-2
Requires: cloud-httpd24-ssl-no-certs

%description
digital-paper-edit

%files

