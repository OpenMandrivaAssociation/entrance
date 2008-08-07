%define	name entrance
%define	version 0.9.9.042
%define cvs 20080202
%define release %mkrel 4.%{cvs}.3

%define major 0
%define libname %mklibname %{name} %major
%define libnamedev %mklibname %{name} -d

Summary: 	Enlightenment login manager
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	BSD
Group: 		Graphical desktop/Enlightenment
URL: 		http://www.enlightenment.org/
Source: 	%{name}-20080202.tar.bz2
Source1:	entrance_config_update.bz2
BuildRoot: 	%{_tmppath}/%{name}-buildroot
BuildRequires:	evas-devel >= 0.9.9.042
BuildRequires:	esmart-devel >= 0.9.0.042
BuildRequires:	ecore-devel >= 0.9.9.042
BuildRequires:	edje-devel >= 0.5.0.042, edje >= 0.5.0.042
Buildrequires:  edb >= 1.0.5.042, embryo >= 0.9.1.042, ecore >= 0.9.9.042
BuildRequires:	efreet-devel >= 0.0.3.042
BuildRequires:	pam-devel
Requires:	ecore >= 0.9.9.042

%description
Entrance is the next generation of Elogin, a login/display manager for
Linux X11 systems. It is designed to be extremely customizable and
aesthetically attractive -- a refreshing relief from the traditional
dull and boring interfaces of XDM and its descendants.

This package is part of the Enlightenment DR17 desktop shell.

%package -n %libname
Summary: Libraries for the %{name} package
Group: System/Libraries

%description -n %libname
Libraries for %{name}

%package -n %libnamedev
Summary: Headers and development libraries from %{name}
Group: Development/Other
Requires: %libname = %{version}
Provides: lib%{name}-devel = %{version}-%{release}
Provides: %name-devel = %{version}-%{release}

%description -n %libnamedev
%{name} development headers and libraries

%prep
%setup -q -n %name

%build
NOCONFIGURE=1 ./autogen.sh
%configure2_5x --with-xbin=%_bindir
#this causes interactive build otherwise, anyway we don't want 
#autodetect.sh, currently tries a free vt (not sure if we need it)
#and copies some pam config (ou rpm already does it)
perl -pi -e "s|sh data/config/autodetect.sh|#sh data/config/autodetect.sh|" Makefile
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
bzcat %SOURCE1 > %buildroot/%_sbindir/entrance_config_update
chmod 755 %buildroot/%_sbindir/entrance_config_update

# make dm config file
mkdir -p %buildroot/%_sysconfdir/X11/dm.d
cat << EOF > %buildroot/%_sysconfdir/X11/dm.d/25entrance.conf
NAME=E17
DESCRIPTION=ENTRANCE (E17 Display Manager)
EXEC=/usr/sbin/entranced
PACKAGE=entrance
FNDSESSION_EXEC="%_sbindir/entrance_config_update -e"
EOF

rm -f %buildroot/%{_sysconfdir}/init.d/%name

cat << EOF > %buildroot/%{_sysconfdir}/pam.d/%name
#%PAM-1.0
auth       required     pam_env.so
auth       include	system-auth
auth       required	pam_nologin.so
account    include	system-auth 
password   include	system-auth
session    include	system-auth
session    optional     pam_console.so
EOF

%post
%make_session

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README
%config(noreplace) %{_sysconfdir}/pam.d/%name
%config(noreplace) %{_sysconfdir}/X11/dm.d/*entrance.conf
%config(noreplace) %{_sysconfdir}/*.cfg
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/%name

%files -n %libname
%defattr(-,root,root)
%{_libdir}/entrance/entrance_login
%{_libdir}/libentrance_edit.so.*

%files -n %libnamedev
%defattr(-,root,root)
%{_includedir}/Entrance_Edit.h
%{_libdir}/libentrance_edit.*a
%{_libdir}/libentrance_edit.so
