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

%description
::package_title::
::package_description_long::

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/mpi3mr-%{version}/
cp -r * %{buildroot}/usr/src/mpi3mr-%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root)
%attr(0755,root,root) /usr/src/mpi3mr-%{version}/

%post
/usr/sbin/dkms add -m mpi3mr -v %{version}
/usr/sbin/dkms build -m mpi3mr -v %{version} && /usr/sbin/dkms install -m mpi3mr -v %{version}
exit 0

%preun
/usr/sbin/dkms remove -m mpi3mr -v %{version} --all
exit 0

%changelog
* Wed Aug 09 2023 Joshua Boudreau <jboudreau@45drives.com> 8.5.1.0.0-45d1
- First build
