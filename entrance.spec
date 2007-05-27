%define	name	entrance
%define	version	0.9.0.009
%define release %mkrel 1

Summary: 	Enlightenment login manager
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	BSD
Group: 		Graphical desktop/Enlightenment
URL: 		http://get-e.org/
Source: 	%{name}-%{version}.tar.bz2
Source1:	entrance_config_update.bz2
BuildRoot: 	%{_tmppath}/%{name}-buildroot
BuildRequires:	evas-devel >= 0.9.9.038, esmart-devel >= 0.9.0.008, edb-devel >= 1.0.5.007
BuildRequires:	ecore-devel >= 0.9.9.038, edje-devel >= 0.5.0.038
Buildrequires:  edje >= 0.5.0.038, edb >= 1.0.5.007, embryo >= 0.9.1.038
BuildRequires:	pam-devel
Requires:	ecore >= 0.9.9.038


%description
Entrance is the next generation of Elogin, a login/display manager for
Linux X11 systems. It is designed to be extremely customizable and
aesthetically attractive -- a refreshing relief from the traditional
dull and boring interfaces of XDM and its descendants.

This package is part of the Enlightenment DR17 desktop shell.

%prep
%setup -q

%build
%configure2_5x
#this causes interactive build otherwise, anyway we don't want 
#autodetect.sh, currently tries a free vt (not sure if we need it)
#and copies some pam config (ou rpm already does it)
perl -pi -e "s|sh data/config/autodetect.sh|#sh data/config/autodetect.sh|" Makefile
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

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

