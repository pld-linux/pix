Summary:	An image viewer and browser utility
Summary(pl.UTF-8):	Przeglądarka obrazków
Name:		pix
Version:	3.4.5
Release:	1
License:	GPL v2+
Group:		X11/Applications/Graphics
#Source0Download: https://github.com/linuxmint/pix/tags
Source0:	https://github.com/linuxmint/pix/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	92dbc1958e19cec44966bd39f3f48f8e
URL:		https://github.com/linuxmint/pix
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	brasero-devel >= 3.2.0
BuildRequires:	clutter-devel >= 1.12.0
BuildRequires:	clutter-gtk-devel >= 1.0.0
BuildRequires:	colord-devel >= 1.3
BuildRequires:	docbook-dtd412-xml
BuildRequires:	exiv2-devel >= 0.21
BuildRequires:	flex
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.54.0
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gstreamer-devel >= 1.0.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0.0
BuildRequires:	gtk+3-devel >= 3.16
# webkit2gtk-4.0 or webkit2-3.0; libsoup3 is not supported yet
BuildRequires:	gtk-webkit4-devel >= 1.10.0
BuildRequires:	json-glib-devel >= 0.15.0
BuildRequires:	lcms2-devel >= 2.6
BuildRequires:	libchamplain-devel >= 0.12
BuildRequires:	libheif-devel >= 1.11
BuildRequires:	libjpeg-devel
BuildRequires:	libjxl-devel >= 0.3.0
BuildRequires:	libpng-devel
BuildRequires:	libraw-devel >= 0.14
BuildRequires:	librsvg-devel >= 2.34.0
BuildRequires:	libsecret-devel >= 0.11
BuildRequires:	libsoup-devel >= 2.42
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtiff-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libwebp-devel >= 0.2.0
BuildRequires:	meson >= 0.43
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
BuildRequires:	xapps-devel >= 2.5.0
BuildRequires:	yelp-tools
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.54.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	brasero-libs >= 3.2.0
Requires:	clutter >= 1.12.0
Requires:	colord >= 1.3
Requires:	exiv2-libs >= 0.21
Requires:	glib2 >= 1:2.54.0
Requires:	gsettings-desktop-schemas
Requires:	gtk+3 >= 3.16
Requires:	gtk-webkit4 >= 1.10.0
Requires:	hicolor-icon-theme
Requires:	json-glib >= 0.15.0
Requires:	lcms2 >= 2.6
Requires:	libchamplain >= 0.12
Requires:	libjxl >= 0.3.0
Requires:	librsvg >= 2.34.0
Requires:	libsecret >= 0.11
Requires:	libsoup >= 2.42
Requires:	libwebp >= 0.2.0
Requires:	xapps >= 2.5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An image viewer and browser utility.

Pix is part of the X-Apps project, which aims at producing
cross-distribution and cross-desktop software.

%description -l pl.UTF-8
Narzędzie do przeglądarnia obrazów.

Pix to część projektu X-Apps, którego celem jest stworzenie
wielodystrybucyjnego, wielośrodowiskowego oprogramowania.

%package devel
Summary:	Pix development files
Summary(pl.UTF-8):	Pliki programistyczne Pix
Group:		X11/Development/Libraries
Requires:	gtk+3-devel >= 3.16

%description devel
This package provides header files for developing Pix extensions.

%description devel -l pl.UTF-8
Ten pakiet dostarcza pliki nagłówkowe potrzebne do rozwijania
rozszerzeń aplikaji Pix.

%prep
%setup -q

# webkit 4.1 uses libsoup-3 while pix links with libsoup-2.4
%{__sed} -i -e 's,webkit2gtk-4\.1,webkit-disabled,' meson.build

%build
%meson \
	-Dlibchamplain=true

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

# not supported by glibc (as of 2.38)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_desktop_database_post
%update_icon_cache hicolor

%postun
%glib_compile_schemas
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS README.md
%attr(755,root,root) %{_bindir}/pix
%dir %{_libdir}/pix
%dir %{_libdir}/pix/extensions
%attr(755,root,root) %{_libdir}/pix/extensions/*.so
%{_libdir}/pix/extensions/*.extension
%{_datadir}/glib-2.0/schemas/org.x.pix.enums.xml
%{_datadir}/glib-2.0/schemas/org.x.pix.gschema.xml
%{_datadir}/glib-2.0/schemas/org.x.pix.*.gschema.xml
%{_datadir}/pix
%{_desktopdir}/pix.desktop
%{_desktopdir}/pix-import.desktop
%{_iconsdir}/hicolor/*x*/apps/pix.png
# XXX: wrong dir
%{_iconsdir}/hicolor/16x16/apps/pix.svg
%{_iconsdir}/hicolor/scalable/apps/pix.svg
%{_mandir}/man1/pix.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/pix
%{_pkgconfigdir}/pix.pc
%{_aclocaldir}/pix.m4
