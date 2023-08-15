Name: ::package_name::
Version: ::package_version::
Release: ::package_build_version::%{?dist}
Summary: ::package_description_short::
License: ::package_licence::
URL: ::package_url::
Source0: %{name}-%{version}.tar.gz
BuildArch: ::package_architecture_el::
Requires: ::package_dependencies_el_el8::

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%global PACKAGE_NAME mpi3mr
%global PACKAGE_VERSION 8.5.1.0.0-45d

%description
::package_title::
::package_description_long::

%prep
%setup -q

%build

%install
echo PACKAGE_NAME=%{PACKAGE_NAME}
echo PACKAGE_VERSION=%{PACKAGE_VERSION}
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/%{PACKAGE_NAME}-%{PACKAGE_VERSION}/
cp -r * %{buildroot}/usr/src/%{PACKAGE_NAME}-%{PACKAGE_VERSION}

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root)
%attr(0755,root,root) /usr/src/%{PACKAGE_NAME}-%{PACKAGE_VERSION}/

%post
/usr/sbin/dkms add -m %{PACKAGE_NAME} -v %{PACKAGE_VERSION}
/usr/sbin/dkms build -m %{PACKAGE_NAME} -v %{PACKAGE_VERSION} && /usr/sbin/dkms install -m %{PACKAGE_NAME} -v %{PACKAGE_VERSION}

%preun
/usr/sbin/dkms remove -m %{PACKAGE_NAME} -v %{PACKAGE_VERSION} --all
exit 0

%changelog
* Tue Aug 15 2023 Joshua Boudreau <jboudreau@45drives.com> 8.5.1.0.0-45d2
- fixed installed path for rocky
* Wed Aug 09 2023 Joshua Boudreau <jboudreau@45drives.com> 8.5.1.0.0-45d1
- First build
