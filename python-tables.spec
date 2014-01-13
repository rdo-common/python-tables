%global with_python3 1

%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_provides_in %{python3_sitearch}/.*\.so$
%filter_setup}

%global module  tables

Summary:        Hierarchical datasets in Python
Name:           python-%{module}
Version:        3.0.0
Release:        3%{?dist}
Source0:        http://sourceforge.net/projects/pytables/files/pytables/%{version}/%{module}-%{version}.tar.gz
Source1:        http://sourceforge.net/project/pytables/pytables/%{version}/pytablesmanual-%{version}.pdf

License:        BSD
Group:          Development/Languages
URL:            http://www.pytables.org
Requires:       numpy
Requires:       python-numexpr

BuildRequires:  hdf5-devel >= 1.8 bzip2-devel lzo-devel
BuildRequires:  Cython >= 0.13 numpy python-numexpr
BuildRequires:  python2-devel

%if 0%{?with_python3}
BuildRequires:  python3-Cython >= 0.13 python3-numpy python3-numexpr >= 2.2
BuildRequires:  python3-devel
%endif # with_python3

%description
PyTables is a package for managing hierarchical datasets and designed
to efficiently and easily cope with extremely large amounts of data.

%if 0%{?with_python3}
%package -n python3-%{module}
Summary:        Hierarchical datasets in Python

Requires:       python3-numpy
Requires:       python3-numexpr

%description -n python3-%{module}
PyTables is a package for managing hierarchical datasets and designed
to efficiently and easily cope with extremely large amounts of data.

This is the version for Python 3.
%endif # with_python3

%package        doc
Group:          Development/Languages
Summary:        Documentation for PyTables
BuildArch:      noarch

%description doc
The %{name}-doc package contains the documentation related to
PyTables.

%prep
%setup -q -n %{module}-%{version}
echo "import tables; tables.test()" > bench/check_all.py
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3
cp -a %{SOURCE1} .

%build
python setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
python3 setup.py build
popd
%endif # with_python3

%check
libdir=`ls build/|grep lib`
export PYTHONPATH=`pwd`/build/$libdir
python bench/check_all.py

%if 0%{?with_python3}
pushd %{py3dir}
libdir=`ls build/|grep lib`
export PYTHONPATH=`pwd`/build/$libdir
python3 bench/check_all.py
popd
%endif # with_python3

%install
chmod -x examples/check_examples.sh
for i in utils/*; do sed -i 's|bin/env |bin/|' $i; done

python setup.py install -O1 --skip-build --root %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
python3 setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif # with_python3


%files
%doc *.txt LICENSES
%{_bindir}/ptdump
%{_bindir}/ptrepack
%{_bindir}/pt2to3
%{python_sitearch}/%{module}
%{python_sitearch}/%{module}-%{version}-py*.egg-info

%if 0%{?with_python3}
%files -n python3-%{module}
%doc *.txt LICENSES
%{python3_sitearch}/%{module}
%{python3_sitearch}/%{module}-%{version}-py*.egg-info
%endif # with_python3

%files doc
%doc pytablesmanual-%{version}.pdf
%doc examples/

%changelog
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
