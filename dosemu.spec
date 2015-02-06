%define	dosver	1.1

#disable for plugins
%define _disable_ld_no_undefined 1

Summary:	DOSEMU stands for DOS Emulation, and enables Linux to run DOS programs
Name:		dosemu
Version:	1.4.0.8
Release:	2
Group:		Emulators
License:	GPLv2+
Url:		http://dosemu.sourceforge.net/
#git archive --format=tar --remote=git://dosemu.git.sourceforge.net/gitroot/dosemu/dosemu dosemu-1.4.0.7 | xz >dosemu-1.4.0.7.tar.xz
Source0:	%{name}-%{version}.tar.xz
Source1:	%{name}-freedos-%{dosver}-bin.tar.bz2
Source11:	xdosemu-16x16.png
Source12:	xdosemu-32x32.png
Source13:	xdosemu-48x48.png
Patch0:		dosemu-1.4.0.8-parallel-build.patch
BuildRequires:	bdftopcf
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	mkfontdir
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(slang)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	gpm-devel
BuildRequires:	svgalib-devel
Requires:	dosimage
Exclusivearch:	%{ix86} x86_64

%description
DOSEMU is a user-level program which uses certain special features
of the Linux kernel and the 80386 processor to run MS-DOS/FreeDOS/
DR-DOS, DOS programs, and many DPMI applications in what we in the
biz call a `DOS box'.

%package -n	xdosemu
Summary:	A DOS emulator for the X Window System
Group:		Emulators
Requires:	%{name} = %{EVRD}
Requires:	dosimage

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
%setup -c %{name} -q -n %{name}-%{version}
%patch0 -p1

bunzip2 -c %{SOURCE1} | gzip -c > freedos.tgz

%build
%configure2_5x	--with-fdtarball=freedos.tgz \
		--with-svgalib \
		--with-x
%make

%install
%makeinstall_std

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

chmod 0755 %{buildroot}%{_libdir}/dosemu/libplugin*.so

%files
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
%{_mandir}/man1/midid.1.*
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
%{_bindir}/xdosemu
%{_mandir}/man1/xdosemu.1*
%lang(ru) %{_mandir}/ru/man1/xdosemu.1*
%{_iconsdir}/hicolor/16x16/apps/x%{name}.png
%{_iconsdir}/hicolor/32x32/apps/x%{name}.png
%{_iconsdir}/hicolor/48x48/apps/x%{name}.png
%{_datadir}/applications/xdosemu.desktop

%files freedos
%{_datadir}/dosemu/freedos-%{dosver}
%{_datadir}/dosemu/drive_z


