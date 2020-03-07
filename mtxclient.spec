Name: mtxclient
Version: 0.2.1
Release: 3%{?dist}
Summary: Client API library for Matrix, built on top of Boost.Asio

License: MIT
URL: https://github.com/Nheko-Reborn/%{name}
Source0: %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires: spdlog-devel >= 0.16
BuildRequires: json-devel >= 3.1.2
BuildRequires: mpark-variant-devel
BuildRequires: libsodium-devel
BuildRequires: openssl-devel
BuildRequires: libolm-devel
BuildRequires: ninja-build
BuildRequires: boost-devel
BuildRequires: zlib-devel
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: gcc

Obsoletes: matrix-structs < %{?epoch:%{epoch}:}%{version}-%{release}

%description
Client API library for the Matrix protocol, built on top of Boost.Asio.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: matrix-structs-devel < %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
# Unpacking main tarball with sources...
%autosetup -p1
mkdir -p %{_target_platform}
sed -i '/-Werror/d' CMakeLists.txt
echo "include_directories(%{_includedir}/nlohmann)" >> CMakeLists.txt
echo "include_directories(%{_includedir}/mpark)" >> CMakeLists.txt

%build
pushd %{_target_platform}
    %cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_LIB_TESTS=OFF \
    -DBUILD_LIB_EXAMPLES=OFF \
    ..
popd
%ninja_build -C %{_target_platform}

%install
%ninja_install -C %{_target_platform}
ln -s libmatrix_client.so.%{version} %{buildroot}%{_libdir}/libmatrix_client.so.0
rm -f %{buildroot}%{_includedir}/{json,variant}.hpp

%files
%doc README.md
%license LICENSE
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}
%{_includedir}/mtx
%{_includedir}/mtx.hpp
%{_libdir}/cmake/MatrixClient
%{_libdir}/*.so

%changelog
* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 23 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 0.2.1-1
- Updated version 0.2.1 (regular release).

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Jonathan Wakely <jwakely@redhat.com> - 0.2.0-3
- Rebuilt for Boost 1.69

* Sat Jan 05 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 0.2.0-2
- Rebuilt due to libolm update.

* Sat Sep 22 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.2.0-1
- Updated version 0.2.0 (regular release).

* Sun Sep 02 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-11
- Obsolete matrix-structs package correctly.

* Sun Sep 02 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-10
- Updated version 0.1.0 (regular release).

* Sun Aug 12 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-9.20180808git1089467
- Updated to latest snapshot.

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.1.0-8.20180726gitca66424
- Rebuild with fixed binutils

* Fri Jul 27 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-7.20180726gitca66424
- Updated to latest snapshot.

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.0-6.20180714git2f519d2
- Rebuild for new binutils

* Thu Jul 26 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-5.20180714git2f519d2
- Minor SPEC fixes.

* Sat Jul 14 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-4.20180714git2f519d2
- Updated to latest snapshot.

* Sun Jul 08 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-3.20180707git708c8c6
- Updated to latest snapshot.

* Sun Jul 01 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-2.20180627git7349126
- Updated to latest snapshot.

* Sun Jun 24 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-2.20180622git96fd35e
- Initial SPEC release.
