%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_provides_in %{python3_sitearch}/.*\.so$
%filter_setup}

%global module  tables

%global commit 16191801a53eddae8ca9380a28988c3b5b263c5e
%global shortcommit %(c=%{commit}; echo ${c:0:7})

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

Summary:        Hierarchical datasets in Python
Name:           python-%{module}
Version:        3.1.2
Release:        3%{?dist}.git%{shortcommit}
Source0:        https://github.com/PyTables/PyTables/archive/%{commit}/PyTables-%{commit}.tar.gz

Source1:        https://sourceforge.net/projects/pytables/files/pytables/%{version}/pytablesmanual-3.1.1.pdf

License:        BSD
Group:          Development/Languages
URL:            http://www.pytables.org
Requires:       numpy
Requires:       python-numexpr

BuildRequires:  hdf5-devel >= 1.8 bzip2-devel lzo-devel
BuildRequires:  Cython >= 0.13 numpy python-numexpr
BuildRequires:  blosc-devel >= 1.5.2
BuildRequires:  python2-devel
BuildRequires:  python3-Cython >= 0.13 python3-numpy python3-numexpr >= 2.2
BuildRequires:  python3-devel

%description
PyTables is a package for managing hierarchical datasets and designed
to efficiently and easily cope with extremely large amounts of data.

This is the version for Python 2.

%package -n python3-%{module}
Summary:        Hierarchical datasets in Python

Requires:       python3-numpy
Requires:       python3-numexpr

%description -n python3-%{module}
PyTables is a package for managing hierarchical datasets and designed
to efficiently and easily cope with extremely large amounts of data.

This is the version for Python 3.

%package        doc
Group:          Development/Languages
Summary:        Documentation for PyTables
BuildArch:      noarch

%description doc
The %{name}-doc package contains the documentation related to
PyTables.

%prep
%setup -q -n PyTables-%{commit}
echo "import tables; tables.test()" > bench/check_all.py
rm -rf %{py3dir}
cp -a . %{py3dir}
cp -a %{SOURCE1} pytablesmanual.pdf

%build
python setup.py build
pushd %{py3dir}
python3 setup.py build
popd

%check
libdir=`ls build/|grep lib`
export PYTHONPATH=`pwd`/build/$libdir
python bench/check_all.py

# OOM during tests on s390
%ifnarch s390
pushd %{py3dir}
libdir=`ls build/|grep lib`
export PYTHONPATH=`pwd`/build/$libdir
python3 bench/check_all.py
popd
%endif

%install
chmod -x examples/check_examples.sh
for i in utils/*; do sed -i 's|bin/env |bin/|' $i; done

python setup.py install -O1 --skip-build --root %{buildroot}
pushd %{py3dir}
python3 setup.py install -O1 --skip-build --root=%{buildroot}
popd


%files
%license LICENSE.txt LICENSES
%{python_sitearch}/%{module}
%{python_sitearch}/%{module}-%{version}*.egg-info

%files -n python3-%{module}
%license LICENSE.txt LICENSES
%{_bindir}/ptdump
%{_bindir}/ptrepack
%{_bindir}/pt2to3
%{_bindir}/pttree
%{python3_sitearch}/%{module}
%{python3_sitearch}/%{module}-%{version}*.egg-info

%files doc
%license LICENSE.txt LICENSES
%doc pytablesmanual.pdf
%doc [A-KM-Za-z]*.txt
%doc examples/

%changelog
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
