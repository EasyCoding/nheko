Summary: Desktop client for the Matrix protocol
Name: nheko
Version: 0.5.4
Release: 1%{?dist}

# Application and 3rd-party modules licensing:
# * S0 - GPLv3+ -- main source.

# Bundled resources licensing:
# * emojione-android fonts - CC by (v4.0) -- bundled resource;
# * OpenSans fonts - Apache (v2.0) -- bundled resource.
License: GPLv3+ and ASL 2.0 and CC-BY
URL: https://github.com/mujx/nheko
Source0: %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires: cmake(Qt5Svg)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5Multimedia)
BuildRequires: cmake(Qt5Concurrent)
BuildRequires: cmake(Qt5LinguistTools)

BuildRequires: spdlog-devel >= 0.16
BuildRequires: json-devel >= 3.1.2
BuildRequires: mpark-variant-devel
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: mtxclient-devel
BuildRequires: libsodium-devel
BuildRequires: openssl-devel
BuildRequires: libolm-devel
BuildRequires: tweeny-devel
BuildRequires: lmdbxx-devel
BuildRequires: ninja-build
BuildRequires: boost-devel
BuildRequires: lmdb-devel
BuildRequires: zlib-devel
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: gcc

Requires: hicolor-icon-theme

%description
The motivation behind the project is to provide a native desktop app
for Matrix that feels more like a mainstream chat app.

%prep
%autosetup -p1
mkdir -p %{_target_platform}
sed -e '/-Wall/d' -e '/-Wextra/d' -e '/-Werror/d' -e '/-pedantic/d' -e '/-pipe/d' -i CMakeLists.txt
echo "set_target_properties(nheko PROPERTIES SKIP_BUILD_RPATH TRUE)" >> CMakeLists.txt
echo "include_directories(%{_includedir}/nlohmann)" >> CMakeLists.txt
echo "include_directories(%{_includedir}/mpark)" >> CMakeLists.txt

%build
pushd %{_target_platform}
    %cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_BUNDLED=OFF \
    ..
popd
%ninja_build -C %{_target_platform}

%install
%ninja_install -C %{_target_platform}

%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%changelog
* Wed Aug 22 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.5.4-1
- Updated to version 0.5.4.

* Wed Aug 15 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.5.3-2
- Backported patch with crash fix on logout.

* Sun Aug 12 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.5.3-1
- Updated to version 0.5.3.

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.5.2-2
- Rebuild with fixed binutils

* Sat Jul 28 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.5.2-1
- Updated to version 0.5.2.

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.1-2
- Rebuild for new binutils

* Thu Jul 26 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.5.1-1
- Updated to version 0.5.1.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.4.3-2
- Fixed issue with system shutdown on KDE Plasma.

* Sun Jun 03 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.4.3-1
- Updated to version 0.4.3.

* Fri May 25 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.4.2-1
- Updated to version 0.4.2.

* Thu May 24 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.4.1-1
- Updated to version 0.4.1.

* Fri May 04 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.4.0-1
- Updated to version 0.4.0.

* Fri Apr 13 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.3.1-1
- Updated to version 0.3.1.

* Tue Apr 03 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.3.0-1
- Updated to version 0.3.0.

* Wed Mar 14 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.2.1-1
- Updated to version 0.2.1.

* Mon Mar 05 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.2.0-1
- Updated to version 0.2.0.

* Thu Dec 28 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-1
- Updated to version 0.1.0.

* Mon Sep 25 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-1.20170924git9def76a
- Initial SPEC release.
