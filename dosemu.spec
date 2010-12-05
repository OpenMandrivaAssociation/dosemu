%define	name	dosemu
%define	version 1.4.0.1
%define	dosver	1.0
%define	release %mkrel 5

#disable for plugins
%define _disable_ld_no_undefined 1

Summary:	DOSEMU stands for DOS Emulation, and enables Linux to run DOS programs
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-1.4.0.tar.bz2
Source1:	%{name}-freedos-%{dosver}-bin.tar.bz2
Source11:	xdosemu-16x16.png
Source12:	xdosemu-32x32.png
Source13:	xdosemu-48x48.png
Patch0:         dosemu-1.4.0.1.diff
Patch1: 	dosemu-1.4.0-dexeconfig-open-O_CREAT-3params.patch
Patch2:		dosemu-1.4.0-fix-str-fmt.patch
# This patch gives a warning when dosemu is run as a user and can't access LOWMEM
# (and users can't by default, for security reasons)
# Next dosemu release should work better, with this kind of message :
#   EXPERIMENTAL: using non-zero memory base address 0x110000.
#   You can use the better-tested zero based setup using
#   sysctl -w vm.mmap_min_addr=0
#   as root, or by changing the vm.mmap_min_addr setting in
#   /etc/sysctl.conf or a file in /etc/sysctl.d/ to 0.
Patch3:		dosemu-1.4.0.1-lowmem-as-user-pb.patch
License:	GPLv2+
Url:		http://dosemu.sourceforge.net/
Group:		Emulators
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	bison flex X11-devel svgalib-devel
BuildRequires:	bdftopcf slang-devel SDL-devel
Requires:	dosimage
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
freedos package, which contains required files which will be
installed in '/usr/share/dosemu/freedos-1.0'

Install dosemu-freedos if you are installing the dosemu package
and you don't have a version of DOS available on your system,
and your system's partitions were not formatted and installed
with DOS.

%prep
%setup -q -n dosemu-1.4.0
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p0

bunzip2 -c %{SOURCE1} | gzip -c > freedos.tgz

%build
%configure2_5x	--with-fdtarball=freedos.tgz \
		--with-svgalib \
		--with-x
%make

%install
rm -rf %{buildroot}
%{makeinstall_std}

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m644 %{SOURCE11} -D \
	%{buildroot}%{_iconsdir}/hicolor/16x16/apps/x%{name}.png
install -m644 %{SOURCE12} -D \
	%{buildroot}%{_iconsdir}/hicolor/32x32/apps/x%{name}.png
install -m644 %{SOURCE13} -D \
	%{buildroot}%{_iconsdir}/hicolor/48x48/apps/x%{name}.png

#xdg menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/xdosemu.desktop <<EOF
[Desktop Entry]
Name=Xdosemu
Comment=DOS emulator running under X
Exec=%{_bindir}/x%{name}
Icon=x%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Emulators;Emulator;
EOF

rm -rf %{buildroot}%{_docdir}

# move freedos to another place to fix update issue (#34837)
mv %{buildroot}%{_datadir}/%{name}/freedos \
 %{buildroot}%{_datadir}/%{name}/freedos-%{dosver}

%if %mdkversion < 200900
%post -n xdosemu
%{update_menus}
%endif

%if %mdkversion < 200900
%postun -n xdosemu
%{clean_menus}
%endif

%clean
rm -rf %{buildroot}

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
%{_iconsdir}/hicolor/16x16/apps/x%{name}.png
%{_iconsdir}/hicolor/32x32/apps/x%{name}.png
%{_iconsdir}/hicolor/48x48/apps/x%{name}.png
%{_datadir}/applications/xdosemu.desktop

%files freedos
%defattr(-,root,root,755)
%{_datadir}/dosemu/freedos-%{dosver}
%{_datadir}/dosemu/drive_z

