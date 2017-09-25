%global commit0 9def76aa0877af373c0b293811c029e268913dc2
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20170924

Summary: Desktop client for the Matrix protocol
Name: nheko
Version: 0
Release: 1.%{date}git%{shortcommit0}%{?dist}

License: GPLv3+
URL: https://github.com/mujx/nheko

Source0: %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires: qt5-qtbase-devel
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: gcc

%description
The motivation behind the project is to provide a native desktop app
for Matrix that feels more like a mainstream chat app (Riot,
Telegram etc) and less like an IRC client.

%prep
%autosetup -n %{name}-%{commit0} -p1

%build
%cmake -DCMAKE_BUILD_TYPE=Release .
%make_build

%install
%make_install

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc README.md
%license COPYING
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%changelog
* Mon Sep 25 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0-1.20170924git9def76a
- Initial SPEC release.
