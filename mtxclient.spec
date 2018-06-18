%global commit0 68188721e042ff5b47ea9a87aa97d3a9efbca989
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20180617

Name: mtxclient
Version: 0.1.0
Release: 1.%{date}git%{shortcommit0}%{?dist}
Summary: Client API library for Matrix, built on top of Boost.Asio

License: MIT
URL: https://github.com/mujx/%{name}
Source0: %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires: spdlog-devel >= 0.16
BuildRequires: matrix-structs-devel
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

%build
pushd %{_target_platform}
    %cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    ..
popd
%ninja_build -C %{_target_platform}

%install
%ninja_install -C %{_target_platform}

%ldconfig_scriptlets

%files
%doc README.md
%license LICENSE
%{_libdir}/*.so

%files devel

%changelog
* Mon Jun 18 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-1.20180617git6818872
- Initial SPEC release.
