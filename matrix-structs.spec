%global commit0 3a052a95c555ce3ae12b8a2e0508e8bb73266fa1
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20180627

Name: matrix-structs
Version: 0.1.0
Release: 2.%{date}git%{shortcommit0}%{?dist}
Summary: De/Serializable types for events, requests/responses and identifiers

License: Public Domain
URL: https://github.com/mujx/%{name}

# * S0 - Public Domain -- main source;
# * S1 (json) - MIT -- build-time dependency (header-only);
# * S1 (variant) - Boost 1.0 -- build-time dependency (header-only).
Source0: %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

# Use ./gen_libs.sh script from repository to generate tarball with header-only libraries...
Source1: header_only-f3b7019.tar.gz
Source2: gen_libs.sh

BuildRequires: ninja-build
BuildRequires: gcc-c++
BuildRequires: doxygen
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
# Unpacking main tarball with sources...
%autosetup -n %{name}-%{commit0} -p1
mkdir -p %{_target_platform}
sed -i '/-Werror/d' CMakeLists.txt
tar -xf %{SOURCE1}

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

%ldconfig_scriptlets

%files
%doc README.md
%license UNLICENSE
%{_libdir}/libmatrix_structs.so.*

%files devel
%{_includedir}/mtx*
%{_libdir}/cmake/MatrixStructs
%{_libdir}/libmatrix_structs.so

%changelog
* Sun Jul 01 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-2.20180627git3a052a9
- Updated to latest snapshot.

* Sun Jun 24 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-2.20180622gitc24cb9b
- Initial SPEC release.
