%global commit0 e4c8a555d6ae48621f6c2c697774fc5052c9e36a
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20171126

%global commit1 0b43ca87d8cfabba392dfe884eb1edb83874de02
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

Summary: Desktop client for the Matrix protocol
Name: nheko
Version: 0
Release: 13.%{date}git%{shortcommit0}%{?dist}

License: GPLv3+
URL: https://github.com/mujx/nheko

Source0: %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1: https://github.com/bendiken/lmdbxx/archive/%{commit1}.tar.gz#/lmdbxx-%{shortcommit1}.tar.gz

Patch0: %{name}-drop-submodules.patch
Patch1: %{name}-drop-flags.patch

BuildRequires: cmake(Qt5LinguistTools)
BuildRequires: desktop-file-utils
BuildRequires: qt5-qtbase-devel
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
%autosetup -n %{name}-%{commit0} -p1

# Unpacking addtional libraries...
pushd libs
    rm -rf lmdbxx
    tar -xf %{SOURCE1}
    mv lmdbxx-%{commit1} lmdbxx
popd

%build
%cmake -DCMAKE_BUILD_TYPE=Release .
%make_build

%install
# Installing binaries...
mkdir -p "%{buildroot}%{_bindir}"
install -m 0755 -p %{name} "%{buildroot}%{_bindir}/%{name}"

# Installing shared libraries...
mkdir -p "%{buildroot}%{_libdir}"
install -m 0755 -p libmatrix_events.so "%{buildroot}%{_libdir}/libmatrix_events.so.0"

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
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
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
%{_libdir}/*.so.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%changelog
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
