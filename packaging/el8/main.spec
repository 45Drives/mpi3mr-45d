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

%define PACKAGE_NAME %(grep PACKAGE_NAME= dkms.conf | cut -d= -f2 | cut -d'"' -f2)
%define PACKAGE_VERSION %(grep PACKAGE_VERSION= dkms.conf | cut -d= -f2 | cut -d'"' -f2)

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
/usr/sbin/dkms add -m %{PACKAGE_NAME} -v %{PACKAGE_VERSION} --rpm_safe_upgrade
/usr/sbin/dkms build -m %{PACKAGE_NAME} -v %{PACKAGE_VERSION} && /usr/sbin/dkms install -m %{PACKAGE_NAME} -v %{PACKAGE_VERSION}

%preun
/usr/sbin/dkms remove -m %{PACKAGE_NAME} -v %{PACKAGE_VERSION} --all --rpm_safe_upgrade
exit 0

%changelog
* Fri Oct 18 2024 Joshua Boudreau <jboudreau@45drives.com> 8.9.1.0.0-45d4
- Fix build in Rocky 9.4 again
* Fri Oct 18 2024 Joshua Boudreau <jboudreau@45drives.com> 8.9.1.0.0-45d3
- Fix build for rocky >= 9.4
* Fri Oct 18 2024 Joshua Boudreau <jboudreau@45drives.com> 8.9.1.0.0-45d2
- Update compat for kernel >= 6.6
* Fri Jul 05 2024 Joshua Boudreau <jboudreau@45drives.com> 8.9.1.0.0-45d1
- Update upstream driver to 8.9.1.0.0
* Fri Jan 05 2024 Joshua Boudreau <jboudreau@45drives.com> 8.7.1.0.0-45d4
- Fix dkms build for rocky
* Thu Dec 07 2023 Joshua Boudreau <jboudreau@45drives.com> 8.7.1.0.0-45d3
- fix generated patch
* Thu Dec 07 2023 Joshua Boudreau <jboudreau@45drives.com> 8.7.1.0.0-45d2
- Update dkms.conf to have proper version
* Thu Dec 07 2023 Joshua Boudreau <jboudreau@45drives.com> 8.7.1.0.0-45d1
- update to 8.7.1
* Fri Aug 18 2023 Joshua Boudreau <jboudreau@45drives.com> 8.6.1.0.0-45d1
- Updated upstream to 8.6.1.0.0
* Tue Aug 15 2023 Joshua Boudreau <jboudreau@45drives.com> 8.5.1.0.0-45d2
- fixed installed path for rocky
* Wed Aug 09 2023 Joshua Boudreau <jboudreau@45drives.com> 8.5.1.0.0-45d1
- First build
