# Git revision of nheko...
%global commit0 48ee36f6b2bcb9d25eec298dda2e77878ab321e1
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20180318

# Git revision of lmdbxx...
%global commit1 0b43ca87d8cfabba392dfe884eb1edb83874de02
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

# Git revision of matrix-structs...
%global commit2 e503c4ff27cd8159c377d9a7d2e6e91698a5517b
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})

# Git revision of tweeny...
%global commit3 b94ce07cfb02a0eb8ac8aaf66137dabdaea857cf
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})

Summary: Desktop client for the Matrix protocol
Name: nheko
Version: 0.2.1
Release: 4.%{date}git%{shortcommit0}%{?dist}

# Application and 3rd-party modules licensing:
# * S0 - GPLv3+ -- main source;
# * S1 (lmdbxx) - Public Domain -- build-time dependency (header-only);
# * S2 (matrix-structs) - Public Domain -- build-time dependency;
# * S3 (tweeny) - MIT -- build-time dependency (header-only);
# * S4 (json) - MIT -- build-time dependency (header-only);
# * S4 (variant) - Boost 1.0 -- build-time dependency (header-only).

# Bundled resources licensing:
# * emojione-android fonts - CC by (v4.0) -- bundled resource;
# * OpenSans fonts - Apache (v2.0) -- bundled resource.
License: GPLv3+ and Public Domain and MIT and Boost and ASL 2.0 and CC-BY
URL: https://github.com/mujx/nheko

# Use ./gen_libs.sh script from repository to generate tarball with header-only libraries...
Source0: %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1: https://github.com/bendiken/lmdbxx/archive/%{commit1}.tar.gz#/lmdbxx-%{shortcommit1}.tar.gz
Source2: https://github.com/mujx/matrix-structs/archive/%{commit2}.tar.gz#/matrix-structs-%{shortcommit2}.tar.gz
Source3: https://github.com/mobius3/tweeny/archive/%{commit3}.tar.gz#/tweeny-%{shortcommit3}.tar.gz
Source4: header_only.tar.gz
Source5: gen_libs.sh

Patch0: %{name}-drop-flags.patch
Patch1: %{name}-drop-rpath.patch

BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5Multimedia)
BuildRequires: cmake(Qt5Concurrent)
BuildRequires: cmake(Qt5LinguistTools)

BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: ninja-build
BuildRequires: lmdb-devel
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: gcc

Requires: hicolor-icon-theme

%description
The motivation behind the project is to provide a native desktop app
for Matrix that feels more like a mainstream chat app.

%prep
# Unpacking main tarball with sources...
%autosetup -n %{name}-%{commit0} -p1
mkdir {%{_target_platform},.third-party}
sed -i '/GIT_/d' cmake/*.cmake

# Unpacking third-party modules...
pushd ".third-party"
    tar -xf %{SOURCE1}
    mv lmdbxx-%{commit1} lmdbxx
    tar -xf %{SOURCE2}
    mv matrix-structs-%{commit2} matrix_structs
    tar -xf %{SOURCE3}
    mv tweeny-%{commit3} tweeny
    pushd matrix_structs
        sed -i 's@add_library(${LIBRARY_NAME} ${SRC})@add_library(${LIBRARY_NAME} STATIC ${SRC})@g' CMakeLists.txt
        tar -xf %{SOURCE4}
    popd
popd

%build
pushd %{_target_platform}
    %cmake -G Ninja -DCMAKE_BUILD_TYPE=Release ..
popd
%ninja_build -C %{_target_platform}

%install
# Installing application...
%ninja_install -C %{_target_platform}

# Installing additional locales...
mkdir -p "%{buildroot}%{_datarootdir}/%{name}/translations"
find %{_target_platform} -maxdepth 1 -type f -name "*.qm" -exec install -m 0644 -p '{}' %{buildroot}%{_datarootdir}/%{name}/translations \;
%find_lang %{name} --with-qt

%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files -f %{name}.lang
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/translations
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%changelog
* Sun Mar 18 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.2.1-4.20180318git48ee36f
- Updated to latest snapshot.

* Sat Mar 17 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.2.1-3.20180317gita6f8673
- Updated to latest snapshot.

* Fri Mar 16 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.2.1-2.20180316git4a6beca
- Updated to latest snapshot.

* Tue Mar 13 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.2.1-1.20180313git1b5e18c
- Updated to version 0.2.1 (snapshot).

* Mon Mar 12 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.2.0-3.20180312git39a8150
- Updated to latest snapshot.

* Sun Mar 11 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.2.0-2.20180311git290de54
- Updated to latest snapshot.

* Mon Mar 05 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.2.0-1.20180304gitd703377
- Updated to version 0.2.0 (snapshot).

* Sun Mar 04 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-30.20180304gitb15a04b
- Updated to latest snapshot.

* Sat Mar 03 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-29.20180303gitb00365f
- Updated to latest snapshot.

* Thu Mar 01 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-28.20180301git735d508
- Updated to latest snapshot.

* Mon Feb 26 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-27.20180226gitc75a136
- Updated to latest snapshot.

* Sat Feb 24 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-26.20180223gitf525b7e
- Updated to latest snapshot.

* Wed Feb 21 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-25.20180220git020f153
- Updated to latest snapshot.

* Tue Feb 20 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-24.20180219git127c52e
- Updated to latest snapshot.

* Mon Feb 19 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-23.20180218gita8e17b9
- Updated to latest snapshot.

* Sun Feb 18 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-22.20180217git7e2f835
- Updated to latest snapshot.

* Sat Feb 17 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-21.20180217git59e4148
- Updated to latest snapshot.

* Fri Feb 16 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-20.20180216gita1ea11d
- Updated to latest snapshot.

* Wed Feb 14 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-19.20180211git6d08e67
- Updated to latest snapshot.

* Sat Feb 10 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-18.20180210gitba8faa3
- Updated to latest snapshot.

* Sat Feb 03 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-17.20180202git43ba4d5
- Updated to latest snapshot.

* Fri Feb 02 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-16.20180202git73bc1ff
- Updated to latest snapshot.

* Thu Feb 01 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-15.20180131git96e9971
- Added AppData manifest. Minor SPEC fixes.

* Thu Feb 01 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-14.20180131git96e9971
- Updated to latest snapshot.

* Wed Jan 31 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-13.20180131git1d7548d
- Updated to latest snapshot.

* Mon Jan 29 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-12.20180129git86aa409
- Updated to latest snapshot.

* Fri Jan 26 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-11.20180125git597f829
- Updated to latest snapshot.

* Thu Jan 25 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-10.20180125git0e91dae
- Updated to latest snapshot.

* Wed Jan 24 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-9.20180123git9eedcd7
- Updated to latest snapshot.

* Mon Jan 22 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-8.20180122git48dabdf
- Updated to latest snapshot.

* Wed Jan 17 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-7.20180117git92a578f
- Updated to latest snapshot.

* Mon Jan 15 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-6.20180114git020a842
- Updated to latest snapshot.

* Sun Jan 14 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-5.20180114git4521837
- Updated to latest snapshot.

* Fri Jan 12 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-4.20180112git396becb
- Updated to latest snapshot.

* Thu Jan 11 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-3.20180111git8beef5e
- Updated to latest snapshot.

* Wed Jan 10 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-2.20180110git7f3b6c4
- Updated to latest snapshot.

* Thu Dec 28 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0.1.0-1
- Updated to version 0.1.0.

* Sun Dec 24 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-28.20171224git6835a97
- Updated to latest snapshot.

* Fri Dec 22 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-27.20171222gita3c1629
- Updated to latest snapshot.

* Thu Dec 21 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-26.20171219git84b5f2b
- Updated to latest snapshot.

* Wed Dec 20 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-25.20171219gitf11044b
- Updated to latest snapshot.

* Mon Dec 18 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-24.20171217git101bf47
- Updated to latest snapshot.

* Sun Dec 17 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-23.20171216git474e52b
- Updated to latest snapshot.

* Sat Dec 16 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-22.20171216gitb5e692b
- Updated to latest snapshot.

* Tue Dec 12 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-21.20171212git6aa635e
- Updated to latest snapshot.

* Mon Dec 11 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-20.20171211git3c5241c
- Updated to latest snapshot.

* Sun Dec 10 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-19.20171210gitbba3bba
- Updated to latest snapshot.

* Thu Dec 07 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-18.20171207git64e4759
- Updated to latest snapshot.

* Wed Dec 06 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-17.20171206gite1a4458
- Updated to latest snapshot.

* Mon Dec 04 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-16.20171204gitb9c4a81
- Updated to latest snapshot.

* Sat Dec 02 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-15.20171201gitf4f78b1
- Updated to latest snapshot.

* Mon Nov 27 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-14.20171127gitf1eb0bb
- Updated to latest snapshot.

* Sun Nov 26 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-13.20171126gite4c8a55
- Updated to latest snapshot.

* Fri Nov 24 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-12.20171124git0f363b5
- Updated to latest snapshot.

* Fri Nov 10 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-11.20171110gite40dab9
- Updated to latest snapshot.

* Thu Nov 09 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-10.20171109gitb586a23
- Updated to latest snapshot.

* Tue Nov 07 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-9.20171107git26904fe
- Updated to latest snapshot.

* Sun Nov 05 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-8.20171105git7a653b2
- Updated to latest snapshot.

* Sat Oct 28 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-7.20171027git845228a
- Updated to latest snapshot.

* Sat Oct 21 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-6.20171021git3cae6c3
- Updated to latest snapshot.

* Sat Oct 21 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-5.20171021git47d1546
- Updated to latest snapshot.

* Wed Oct 18 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-4.20171016git8390ff2
- Updated to latest snapshot.

* Tue Oct 10 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-3.20171010git7748529
- Updated to latest snapshot.

* Mon Oct 09 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-2.20171009git513f69e
- Updated to latest snapshot.

* Mon Sep 25 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-1.20170924git9def76a
- Initial SPEC release.
