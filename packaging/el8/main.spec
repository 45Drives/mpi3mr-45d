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

%global PACKAGE_NAME %(grep PACKAGE_NAME= dkms.conf | cut -d= -f2 | cut -d\" -f2)
%global PACKAGE_VERSION %(grep PACKAGE_VERSION= dkms.conf | cut -d= -f2 | cut -d\" -f2)

%description
::package_title::
::package_description_long::

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/%(grep PACKAGE_NAME= dkms.conf | cut -d= -f2 | cut -d\" -f2)-%(grep PACKAGE_VERSION= dkms.conf | cut -d= -f2 | cut -d\" -f2)/
cp -r * %{buildroot}/usr/src/%(grep PACKAGE_NAME= dkms.conf | cut -d= -f2 | cut -d\" -f2)-%(grep PACKAGE_VERSION= dkms.conf | cut -d= -f2 | cut -d\" -f2)

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root)
%attr(0755,root,root) /usr/src/%(grep PACKAGE_NAME= dkms.conf | cut -d= -f2 | cut -d\" -f2)-%(grep PACKAGE_VERSION= dkms.conf | cut -d= -f2 | cut -d\" -f2)/

%post
/usr/sbin/dkms add -m %(grep PACKAGE_NAME= dkms.conf | cut -d= -f2 | cut -d\" -f2) -v %(grep PACKAGE_VERSION= dkms.conf | cut -d= -f2 | cut -d\" -f2)
/usr/sbin/dkms build -m %(grep PACKAGE_NAME= dkms.conf | cut -d= -f2 | cut -d\" -f2) -v %(grep PACKAGE_VERSION= dkms.conf | cut -d= -f2 | cut -d\" -f2) && /usr/sbin/dkms install -m %(grep PACKAGE_NAME= dkms.conf | cut -d= -f2 | cut -d\" -f2) -v %(grep PACKAGE_VERSION= dkms.conf | cut -d= -f2 | cut -d\" -f2)

%preun
/usr/sbin/dkms remove -m %(grep PACKAGE_NAME= dkms.conf | cut -d= -f2 | cut -d\" -f2) -v %(grep PACKAGE_VERSION= dkms.conf | cut -d= -f2 | cut -d\" -f2) --all
exit 0

%changelog
* Tue Aug 15 2023 Joshua Boudreau <jboudreau@45drives.com> 8.5.1.0.0-45d2
- fixed installed path for rocky
* Wed Aug 09 2023 Joshua Boudreau <jboudreau@45drives.com> 8.5.1.0.0-45d1
- First build
