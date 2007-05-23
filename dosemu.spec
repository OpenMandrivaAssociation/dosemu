%define	name	dosemu
%define	version 1.4.0
%define	dosver	1.0
%define	release %mkrel 1

Summary:	DOSEMU stands for DOS Emulation, and enables Linux to run DOS programs
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-freedos-%{dosver}-bin.tar.bz2
Source11:	xdosemu-16x16.png
Source12:	xdosemu-32x32.png
Source13:	xdosemu-48x48.png
License:	GPL
Url:		http://www.dosemu.org/
Group:		Emulators
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	bison flex XFree86 XFree86-devel svgalib-devel
BuildRequires:	bdftopcf slang-devel
Exclusivearch:	%{ix86}

%description
DOSEMU is a user-level program which uses certain special features
of the Linux kernel and the 80386 processor to run MS-DOS/FreeDOS/
DR-DOS, DOS programs, and many DPMI applications in what we in the
biz call a `DOS box'.

%package -n	xdosemu
Requires:	%{name} = %{version}-%{release} dosimage
Summary:	A DOS emulator for the X Window System
Group:		Emulators

%description -n xdosemu
Xdosemu is a version of the dosemu DOS emulator that runs with the X
Window System.  Xdosemu provides VGA graphics and mouse support.

Install xdosemu if you need to run DOS programs on your system, and you'd
like to do so with the convenience of graphics support and mouse
capabilities.

%package	freedos
Summary:	A FreeDOS hdimage for dosemu, a DOS emulator, to use
Group:		Emulators
Provides:	dosimage

%description freedos
Generally, the dosemu DOS emulator requires either that your system
have some version of DOS available or that your system's partitions
were formatted and installed with DOS. If your system does not meet
either of the previous requirements, you can instead use the dosemu-
freedos package, which contains an hdimage file which will be
installed in the /var/lib/dosemu directory. The hdimage file is
already bootable with FreeDOS.

You will need to edit your /etc/dosemu.conf file to add the
image to the list of disk 'drives' used by dosemu.

Install dosemu-freedos if you are installing the dosemu package
and you don't have a version of DOS available on your system,
and your system's partitions were not formatted and installed
with DOS.

%prep
%setup -q
bunzip2 -c %{SOURCE1} | gzip -c > freedos.tgz

%build
%configure2_5x	--with-fdtarball=freedos.tgz \
		--with-svgalib \
		--with-x
%make

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std}

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/xdosemu.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/xdosemu.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/xdosemu.png

# (fg) Menu entry for xdos
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat >$RPM_BUILD_ROOT%{_menudir}/xdosemu <<EOF
?package(xdosemu):command="%{_bindir}/xdosemu" needs="X11" icon="xdosemu.png" \
section="More Applications/Emulators" title="DOS emulator" \
longtitle="DOS emulator running under X" xdg="true"
EOF

#xdg menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/xdosemu.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=Xdosemu
Comment=DOS emulator running under X
Exec=%{_bindir}/x%{name}
Icon=x%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Emulators;Emulator;
EOF

rm -rf $RPM_BUILD_ROOT%{_docdir}

%post -n xdosemu
# (fg) For the menu entry
%{update_menus}

%postun -n xdosemu
# (fg) For the menu entry
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc/*
%{_bindir}/dosemu.bin
%{_bindir}/dosemu
%{_bindir}/mkfatimage
%{_bindir}/mkfatimage16
%{_bindir}/midid
%{_bindir}/dosdebug
%{_libdir}/dosemu/libplugin*.so
%{_mandir}/man1/mkfatimage16.1*
%{_mandir}/man1/dosdebug.1*
%{_mandir}/man1/dosemu.1*
%{_mandir}/man1/dosemu.bin.1*
%lang(ru) %{_mandir}/ru/man1/mkfatimage16.1*
%lang(ru) %{_mandir}/ru/man1/dosdebug.1*
%lang(ru) %{_mandir}/ru/man1/dosemu.1*
%lang(ru) %{_mandir}/ru/man1/dosemu.bin.1*
%{_datadir}/dosemu/commands
%{_datadir}/dosemu/keymap
%{_datadir}/dosemu/Xfonts
%config(noreplace) %{_sysconfdir}/dosemu.conf
%config(noreplace) %{_sysconfdir}/drives/c
%config(noreplace) %{_sysconfdir}/drives/d
%config(noreplace) %{_sysconfdir}/dosemu.users
%config(noreplace) %{_sysconfdir}/global.conf

%files -n xdosemu
%defattr(-,root,root,755)
%{_bindir}/xdosemu
%{_mandir}/man1/xdosemu.1*
%lang(ru) %{_mandir}/ru/man1/xdosemu.1*
%{_menudir}/xdosemu
%{_miconsdir}/xdosemu.png
%{_liconsdir}/xdosemu.png
%{_iconsdir}/xdosemu.png
%{_datadir}/applications/xdosemu.desktop

%files freedos
%defattr(-,root,root,755)
%{_datadir}/dosemu/freedos
%{_datadir}/dosemu/drive_z

