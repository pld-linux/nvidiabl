#
# Conditional build:
%bcond_without	verbose		# verbose build (V=1)
%bcond_without	dkms		# build dkms package

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		_duplicate_files_terminate_build	0

%define		rel	1
%define		pname	nvidiabl
Summary:	Linux driver for nVidia display back-lights
Summary(pl.UTF-8):	Sterownik dla Linuksa do podświetlania wyświetlacza dla kart firmy nVidia
Name:		%{pname}%{_alt_kernel}
Version:	0.87
Release:	%{rel}%{?_pld_builder:@%{_kernel_ver_str}}
License:	GPL v2+
Group:		Base/Kernel
Source0:	https://github.com/guillaumezin/nvidiabl/archive/v%{version}.tar.gz?/%{pname}-%{version}.tgz
Source1:	modprobe.conf
Patch0:		nvidiabl-dkmsconf.patch
# Source0-md5:	e9418d3e500172d79680e44ad0f85743
URL:		https://github.com/guillaumezin/nvidiabl
BuildRequires:	rpmbuild(macros) >= 1.701
%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This driver drives the smartdimmer register found on modern mobile
nVidia graphics adapters such as NV40, NV41, NV43, NV44, NV46, NV47,
NV49, NV4B, C51, G84, G86, G92, G94, G96, GT200 architectures to
adjust the display backlight.

On Apple machines this driver allows more fine-grained brightness
adjustment than the (mbp_nvidia_bl) driver and is generally preferred.

%description -l pl.UTF-8
Ten sterownik steruje rejestrem "smartdimmer" obecnym we współczesnych
mobilnych kartach graficznych firmy nVidia (takich jak architektury
NV40, NV41, NV43, NV44, NV46, NV47, NV49, NV4B, C51, G84, G86, G92,
G94, G96, GT200), służącym do regulacji podświetlenia wyświetlacza.

Na komputerach firmy Apple ten sterownik pozwala na dokładniejsze
ustawianie jasności niż sterownik mbp_nvidia_bl i ogólnie jest
zalecany.

%package -n dkms-%{pname}
Summary:	DKMS-ready driver for nVidia display back-lights
Summary(pl.UTF-8):	Sterownik zgodny z DKMS do podświetlania wyświetlacza dla kart firmy nVidia
License:	GPL v2+
Group:		Base/Kernel
Requires(pre,post):	dkms
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n dkms-%{pname}
This package contains a DKMS-ready driver for nVidia laptop display
back-lights.

This driver drives the smartdimmer register found on modern mobile
Nvidia graphics adapters such as NV40, NV41, NV43, NV44, NV46, NV47,
NV49, NV4B, C51, G84, G86, G92, G94, G96, GT200 architectures to
adjust the display backlight.

On Apple machines this driver allows more fine-grained brightness
adjustment than the mbp-nvidia-bl-dkms (mbp_nvidia_bl) driver and is
generally preferred.

%description -n dkms-%{pname} -l pl.UTF-8
Ten pakiet zawiera zgodny z DKMS sterownik do podświetlania
wyświetlacza laptopów z kartą graficzną firmy nVidia.

Ten sterownik steruje rejestrem "smartdimmer" obecnym we współczesnych
mobilnych kartach graficznych firmy nVidia (takich jak architektury
NV40, NV41, NV43, NV44, NV46, NV47, NV49, NV4B, C51, G84, G86, G92,
G94, G96, GT200), służącym do regulacji podświetlenia wyświetlacza.

Na komputerach firmy Apple ten sterownik pozwala na dokładniejsze
ustawianie jasności niż sterownik mbp_nvidia_bl i ogólnie jest
zalecany.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-video-nvidiabl\
Summary:	Linux driver for nVidia display back-lights\
Summary(pl.UTF-8):	Sterownik dla Linuksa do podświetlania wyświetlacza dla kart firmy nVidia\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
\
%description -n kernel%{_alt_kernel}-video-nvidiabl\
This driver drives the smartdimmer register found on modern mobile\
nVidia graphics adapters such as NV40, NV41, NV43, NV44, NV46, NV47,\
NV49, NV4B, C51, G84, G86, G92, G94, G96, GT200 architectures to\
adjust the display backlight.\
\
On Apple machines this driver allows more fine-grained brightness\
adjustment than the (mbp_nvidia_bl) driver and is generally preferred.\
\
%description -n kernel%{_alt_kernel}-video-nvidiabl -l pl.UTF-8\
Ten sterownik steruje rejestrem "smartdimmer" obecnym we współczesnych\
mobilnych kartach graficznych firmy nVidia (takich jak architektury\
NV40, NV41, NV43, NV44, NV46, NV47, NV49, NV4B, C51, G84, G86, G92,\
G94, G96, GT200), służącym do regulacji podświetlenia wyświetlacza.\
\
Na komputerach firmy Apple ten sterownik pozwala na dokładniejsze\
ustawianie jasności niż sterownik mbp_nvidia_bl i ogólnie jest\
zalecany.\
\
%files -n kernel%{_alt_kernel}-video-nvidiabl\
%defattr(644,root,root,755)\
/lib/modules/%{_kernel_ver}/misc/*.ko*\
%config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/%{pname}.conf\
\
%post	-n kernel%{_alt_kernel}-video-nvidiabl\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-video-nvidiabl\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%build_kernel_modules -m nvidiabl\
%install_kernel_modules -D installed -m nvidiabl -d misc\
%{nil}

%{expand:%create_kernel_packages}

%prep
%setup -qn %{pname}-%{version}
%patch0 -p1

%build
%{expand:%build_kernel_packages}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/modprobe.d

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/modprobe.d/%{pname}.conf
cp -a installed/* $RPM_BUILD_ROOT

%if %{with dkms}
install -d $RPM_BUILD_ROOT%{_usrsrc}/%{pname}-%{version}-%{rel}
cp -p Makefile *.[ch] $RPM_BUILD_ROOT%{_usrsrc}/%{pname}-%{version}-%{rel}
sed -e 's|@pname@|%{pname}|g' -e 's|@MODVERSION@|%{version}-%{rel}|g' \
	dkms.conf > $RPM_BUILD_ROOT%{_usrsrc}/%{pname}-%{version}-%{rel}/dkms.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n dkms-%{pname}
%{_sbindir}/dkms add -m %{pname} -v %{version}-%{rel} --rpm_safe_upgrade && \
%{_sbindir}/dkms build -m %{pname} -v %{version}-%{rel} --rpm_safe_upgrade && \
%{_sbindir}/dkms install -m %{pname} -v %{version}-%{rel} --rpm_safe_upgrade || :

%preun -n dkms-%{pname}
%{_sbindir}/dkms remove -m %{pname} -v %{version}-%{rel} --rpm_safe_upgrade --all || :

%if %{with dkms}
%files -n dkms-%{pname}
%defattr(644,root,root,755)
%{_usrsrc}/%{pname}-%{version}-%{rel}
%endif
