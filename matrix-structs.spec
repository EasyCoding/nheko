%global commit0 56b5b58889c70d47139e60c3bfb2a921d5a35b41
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20180808

Name: matrix-structs
Version: 0.1.0
Release: 8.%{date}git%{shortcommit0}%{?dist}
Summary: De/Serializable types for events, requests/responses and identifiers

License: Public Domain
URL: https://github.com/mujx/%{name}
Source0: %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

Patch0: %{name}-unbundle-libs.patch

BuildRequires: mpark-variant-devel
BuildRequires: json-devel >= 3.1.2
BuildRequires: ninja-build
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: gcc

%description
Collection of structs used in the Matrix protocol with built in
serialization/deserialization to/from json.

There is support for:

 * events;
 * matrix identifiers;
 * request types;
 * response types.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{commit0} -p1
mkdir -p %{_target_platform}
sed -i '/-Werror/d' CMakeLists.txt
echo "include_directories(%{_includedir}/nlohmann)" >> CMakeLists.txt
echo "include_directories(%{_includedir}/mpark)" >> CMakeLists.txt

%build
pushd %{_target_platform}
    %cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    ..
popd
%ninja_build -C %{_target_platform}

%install
%ninja_install -C %{_target_platform}
ln -s libmatrix_structs.so.%{version} %{buildroot}%{_libdir}/libmatrix_structs.so.0
rm -f %{buildroot}%{_includedir}/{json,variant}.hpp

%files
%doc README.md
%license UNLICENSE
%{_libdir}/libmatrix_structs.so.*

%files devel
%{_includedir}/mtx*
%{_libdir}/cmake/MatrixStructs
%{_libdir}/libmatrix_structs.so

%changelog
* Sun Aug 12 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-8.20180808git56b5b58
- Updated to latest snapshot.

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.1.0-7.20180714git8de04af
- Rebuild with fixed binutils

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.0-6.20180714git8de04af
- Rebuild for new binutils

* Thu Jul 26 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-5.20180714git8de04af
- Minor SPEC fixes.

* Sat Jul 14 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-4.20180714git8de04af
- Updated to latest snapshot.

* Sun Jul 08 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-3.20180707git92a5e99
- Updated to latest snapshot.

* Sun Jul 01 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-2.20180627git3a052a9
- Updated to latest snapshot.

* Sun Jun 24 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-2.20180622gitc24cb9b
- Initial SPEC release.
