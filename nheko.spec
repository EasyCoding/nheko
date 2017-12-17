# Git revision of nheko...
%global commit0 474e52b5020eb1db2a30f9b505cc0d1c7a1ca780
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20171216

# Git revision of lmdbxx...
%global commit1 0b43ca87d8cfabba392dfe884eb1edb83874de02
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

# Git revision of matrix-structs...
%global commit2 94fc20545429d57c7424df55d51b5d2e4bc7d6b5
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})

Summary: Desktop client for the Matrix protocol
Name: nheko
Version: 0
Release: 23.%{date}git%{shortcommit0}%{?dist}

License: GPLv3+
URL: https://github.com/mujx/nheko

# Use ./gen_libs.sh script from repository to generate tarball with header-only libraries...
Source0: %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1: https://github.com/bendiken/lmdbxx/archive/%{commit1}.tar.gz#/lmdbxx-%{shortcommit1}.tar.gz
Source2: https://github.com/mujx/matrix-structs/archive/%{commit2}.tar.gz#/matrix-structs-%{shortcommit2}.tar.gz
Source3: header_only.tar.gz

Patch0: %{name}-drop-submodules.patch
Patch1: %{name}-drop-flags.patch
Patch2: %{name}-drop-rpath.patch

BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5Multimedia)
BuildRequires: cmake(Qt5Concurrent)
BuildRequires: cmake(Qt5LinguistTools)

BuildRequires: desktop-file-utils
BuildRequires: lmdb-devel
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: gcc

%description
The motivation behind the project is to provide a native desktop app
for Matrix that feels more like a mainstream chat app (Riot,
Telegram etc) and less like an IRC client.

%prep
# Unpacking main tarball with sources...
%autosetup -n %{name}-%{commit0}

# Unpacking lmdbxx...
pushd libs
    rm -rf lmdbxx
    tar -xf %{SOURCE1}
    mv lmdbxx-%{commit1} lmdbxx
popd

# Unpacking matrix-structs...
pushd libs
    rm -rf matrix-structs
    tar -xf %{SOURCE2}
    mv matrix-structs-%{commit2} matrix-structs
    pushd matrix-structs
        sed -i 's@add_library(${LIBRARY_NAME} ${SRC})@add_library(${LIBRARY_NAME} STATIC ${SRC})@g' CMakeLists.txt
        tar -xf %{SOURCE3}
    popd
popd

%build
%cmake -DCMAKE_BUILD_TYPE=Release .
%make_build

%install
# Installing binaries...
mkdir -p "%{buildroot}%{_bindir}"
install -m 0755 -p %{name} "%{buildroot}%{_bindir}/%{name}"

# Installing icons...
for size in 16 32 48 64 128 256 512; do
    dir="%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps"
    install -d "$dir"
    install -m 0644 -p resources/%{name}-${size}.png "$dir/%{name}.png"
done

# Installing desktop shortcut...
desktop-file-install --dir="%{buildroot}%{_datadir}/applications" resources/%{name}.desktop

# Installing additional locales...
mkdir -p "%{buildroot}%{_datarootdir}/%{name}/translations"
find . -maxdepth 1 -type f -name "*.qm" -exec install -m 0644 -p '{}' %{buildroot}%{_datarootdir}/%{name}/translations \;
%find_lang %{name} --with-qt

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%changelog
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
