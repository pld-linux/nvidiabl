#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
%bcond_with	dkms	# build dkms package

%if "%{_alt_kernel}" != "%{nil}"
%if 0%{?build_kernels:1}
%{error:alt_kernel and build_kernels are mutually exclusive}
exit 1
%endif
%global		_build_kernels		%{alt_kernel}
%else
%global		_build_kernels		%{?build_kernels:,%{?build_kernels}}
%endif

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		_duplicate_files_terminate_build	0

%define		kbrs	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo "BuildRequires:kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2" ; done)
%define		kpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%kernel_pkg ; done)
%define		bkpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%build_kernel_pkg ; done)

%define		rel	29
%define		pname	nvidiabl
Summary:	Linux driver for nVidia display back-lights
Name:		%{pname}%{_alt_kernel}
Version:	0.81
Release:	%{rel}%{?_pld_builder:@%{_kernel_ver_str}}
License:	GPL v2+
URL:		https://github.com/guillaumezin/nvidiabl
Source0:	https://github.com/guillaumezin/nvidiabl/archive/v%{version}.tar.gz?/%{pname}-%{version}.tgz
# Source0-md5:	f72d90c0fe34b36a0ff3b6d7034e99c4
Source1:	modprobe.conf
Patch0:		nvidiabl-dkmsconf.patch
Group:		Base/Kernel
BuildRequires:	rpmbuild(macros) >= 1.678
%{?with_dist_kernel:%{expand:%kbrs}}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This driver drives the smartdimmer register found on modern mobile
nVidia graphics adapters such as NV40, NV41, NV43, NV44, NV46, NV47,
NV49, NV4B, C51, G84, G86, G92, G94, G96, GT200 architectures to
adjust the display backlight.

On Apple machines this driver allows more fine-grained brightness
adjustment than the (mbp_nvidia_bl) driver and is generally preferred.

%package -n dkms-%{pname}
Summary:	DKMS-ready driver for nVidia display back-lights
License:	GPL v2+
Group:		Base/Kernel
Requires(pre):	dkms
Requires(post):	dkms
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n dkms-%{pname}
This package contains a DKMS-ready driver for nvidia laptop display
back-lights.

This driver drives the smartdimmer register found on modern mobile
Nvidia graphics adapters such as NV40, NV41, NV43, NV44, NV46, NV47,
NV49, NV4B, C51, G84, G86, G92, G94, G96, GT200 architectures to
adjust the display backlight.

On Apple machines this driver allows more fine-grained brightness
adjustment than the mbp-nvidia-bl-dkms (mbp_nvidia_bl) driver and is
generally preferred.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-video-nvidiabl\
Summary:	Linux driver for nVidia display back-lights\
Summary(pl.UTF-8):	Sterownik dla Linuksa do nvidiabl\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%if %{with dist_kernel}\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
%endif\
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
Sterownik dla Linuksa do nvidiabl.\
\
Ten pakiet zawiera moduł jądra Linuksa.\
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

%{expand:%kpkg}

%prep
%setup -qn %{pname}-%{version}
%patch0 -p1

%build
%{expand:%bkpkg}

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
