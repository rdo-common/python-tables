#global commit 16191801a53eddae8ca9380a28988c3b5b263c5e
%{?gitcommit:%global gitcommitshort %(c=%{gitcommit}; echo ${c:0:7})}

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

Summary:        HDF5 support in Python
Name:           python-tables
Version:        3.3.0
Release:        2%{?dist}%{?gitcommit:.git%{shortcommit}}
#Source0:        https://github.com/PyTables/PyTables/archive/%{commit}/PyTables-%{commit}.tar.gz
Source0:        https://github.com/PyTables/PyTables/archive/v%{version}.tar.gz#/python-tables-%{version}.tar.gz

Source1:        https://github.com/PyTables/PyTables/releases/download/v%{version}/pytablesmanual-%{version}.pdf
Patch0:         always-use-blosc.diff
Patch1:         0001-setup.py-gracefuly-handle-cpuinfo-failure.patch

License:        BSD
URL:            http://www.pytables.org

BuildRequires:  hdf5-devel >= 1.8 bzip2-devel lzo-devel
BuildRequires:  Cython >= 0.13
BuildRequires:  numpy
BuildRequires:  python-numexpr >= 2.4
BuildRequires:  blosc-devel >= 1.5.2
BuildRequires:  python2-devel
BuildRequires:  python2-six
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-Cython >= 0.13
BuildRequires:  python%{python3_pkgversion}-numpy
BuildRequires:  python%{python3_pkgversion}-numexpr >= 2.4
BuildRequires:  python%{python3_pkgversion}-six

%description
PyTables is a package for managing hierarchical datasets and designed
to efficiently and easily cope with extremely large amounts of data.

%package -n python2-tables
Summary:        %{summary}

Requires:       numpy
Requires:       python2-six
Requires:       python2-numexpr >= 2.4
%{?python_provide:%python_provide python2-tables}

%description -n python2-tables
PyTables is a package for managing hierarchical datasets and designed
to efficiently and easily cope with extremely large amounts of data.

This is the version for Python 2.

%package -n python%{python3_pkgversion}-tables
Summary:        %{summary}

Requires:       python%{python3_pkgversion}-numpy
Requires:       python%{python3_pkgversion}-six
Requires:       python%{python3_pkgversion}-numexpr >= 2.4
%{?python_provide:%python_provide python%{python3_pkgversion}-tables}

%description -n python%{python3_pkgversion}-tables
PyTables is a package for managing hierarchical datasets and designed
to efficiently and easily cope with extremely large amounts of data.

This is the version for Python 3.

%package        doc
Group:          Development/Languages
Summary:        Documentation for PyTables
BuildArch:      noarch

%description doc
The %{name}-doc package contains the documentation for %{name}.

%prep
%autosetup -n PyTables-%{version} -p1
cp -a %{SOURCE1} pytablesmanual.pdf

echo "import sys, tables; sys.exit(tables.test(verbose=1))" > bench/check_all.py

# Make sure we are not using anything from the bundled blosc by mistake
find c-blosc -mindepth 1 -maxdepth 1 -name hdf5 -prune -o -exec rm -r {} +

%build
%py2_build
%py3_build

%install
chmod -x examples/check_examples.sh
sed -i 's|bin/env |bin/|' utils/*

%py2_install
%py3_install

%check
export LANG=en_US.UTF-8
PYTHONPATH=%{buildroot}%{python2_sitearch} %{__python2} bench/check_all.py

# OOM during tests on s390
%ifnarch s390
PYTHONPATH=%{buildroot}%{python3_sitearch} %{__python3} bench/check_all.py
%endif

%files -n python2-tables
%license LICENSE.txt LICENSES
%{python2_sitearch}/tables
%{python2_sitearch}/tables-%{version}*.egg-info

%files -n python%{python3_pkgversion}-tables
%license LICENSE.txt LICENSES
%{_bindir}/ptdump
%{_bindir}/ptrepack
%{_bindir}/pt2to3
%{_bindir}/pttree
%{python3_sitearch}/tables
%{python3_sitearch}/tables-%{version}*.egg-info

%files doc
%license LICENSE.txt LICENSES
%doc pytablesmanual.pdf
%doc [A-KM-Za-z]*.txt
%doc examples/

%changelog
* Mon Nov 07 2016 Than Ngo <than@redhat.com> - 3.3.0-2
- rebuild against new blosc due to big endien issue on s390x/ppc64

* Thu Sep 15 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.3.0-1
- Update to latest upstream version (#1352621)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 17 2016 Orion Poplawski <orion@cora.nwra.com> - 3.2.2-5
- Update provides filter
- Ship python2 package
- Use %%python3_pkgversion for EPEL7 compatibility
- Use current python macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Orion Poplawski <orion@cora.nwra.com> - 3.2.2-3
- Rebuild for hdf5 1.8.16

* Wed Nov 18 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.2-2
- Make sure numexpr is new enough

* Sat Nov 14 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.2-1
- Update to latest version

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 3.2.0-2
- Rebuild for hdf5 1.8.15

* Thu May  7 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.0-1
- Update to 3.2.0

* Thu Jan  8 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.1.2-4.git1619180
- Use blosc on all architectures

* Thu Jan  8 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.1.2-3.git1619180
- Update to latest snapshot and use external blosc

* Wed Jan 07 2015 Orion Poplawski <orion@cora.nwra.com> - 3.1.1-2
- Rebuild for hdf5 1.8.14

* Tue Jan 06 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.1.1-1
- Update to 3.1.1 (#1080889)

* Tue Nov 25 2014 Dan Horák <dan[at]danny.cz> - 3.0.0-8
- workaround OOM during Python3 tests on s390

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar 24 2014 Zbigniew Jędrzejewski-Szmek - 3.0.0-4
- Rebuild for latest blosc

* Fri Jan 10 2014 Zbigniew Jędrzejewski-Szmek - 3.0.0-3
- Move python3 requires to the proper package (#1051691)

* Thu Sep 05 2013 Zbigniew Jędrzejewski-Szmek - 3.0.0-2
- Add python3-tables package

* Wed Aug 21 2013 Thibault North <tnorth@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 2.4.0-3
- Rebuild for hdf5 1.8.11

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct 28 2012 Thibault North <tnorth@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Thibault North <tnorth@fedoraproject.org> - 2.3.1-3
- Remove lrucache.py which was deprecated and under AFL license

* Thu Nov 10 2011 Thibault North <tnorth@fedoraproject.org> - 2.3.1-2
- Fixes and subpackage for the docs

* Mon Nov 07 2011 Thibault North <tnorth@fedoraproject.org> - 2.3.1-1
- Fixes and update to 2.3.1
