%global commit0 2f519d28b4521f7f234b2ed0f32360cbb1edd2f7
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20180714

Name: mtxclient
Version: 0.1.0
Release: 6.%{date}git%{shortcommit0}%{?dist}
Summary: Client API library for Matrix, built on top of Boost.Asio

License: MIT
URL: https://github.com/mujx/%{name}
Source0: %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires: spdlog-devel >= 0.16
BuildRequires: matrix-structs-devel
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

%description
Client API library for the Matrix protocol, built on top of Boost.Asio.

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
%{_libdir}/cmake/MatrixClient
%{_libdir}/*.so

%changelog
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
