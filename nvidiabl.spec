#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)
%bcond_with	dkms	# build dkms package

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		rel	11
%define		modname	nvidiabl
Summary:	Linux driver for nVidia display back-lights
Name:		%{modname}%{_alt_kernel}
Version:	0.81
Release:	%{rel}
License:	GPL v2+
URL:		https://github.com/guillaumezin/nvidiabl
Source0:	https://github.com/guillaumezin/nvidiabl/archive/v%{version}.tar.gz?/%{modname}-%{version}.tgz
# Source0-md5:	f72d90c0fe34b36a0ff3b6d7034e99c4
Source1:	modprobe.conf
Patch0:		nvidiabl-dkmsconf.patch
Group:		Base/Kernel
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This driver drives the smartdimmer register found on modern mobile
nVidia graphics adapters such as NV40, NV41, NV43, NV44, NV46, NV47,
NV49, NV4B, C51, G84, G86, G92, G94, G96, GT200 architectures to
adjust the display backlight.

On Apple machines this driver allows more fine-grained brightness
adjustment than the (mbp_nvidia_bl) driver and is generally preferred.

%package -n dkms-%{modname}
Summary:	DKMS-ready driver for nVidia display back-lights
License:	GPL v2+
Group:		Base/Kernel
Requires(pre):	dkms
Requires(post):	dkms
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n dkms-%{modname}
This package contains a DKMS-ready driver for nvidia laptop display
back-lights.

This driver drives the smartdimmer register found on modern mobile
Nvidia graphics adapters such as NV40, NV41, NV43, NV44, NV46, NV47,
NV49, NV4B, C51, G84, G86, G92, G94, G96, GT200 architectures to
adjust the display backlight.

On Apple machines this driver allows more fine-grained brightness
adjustment than the mbp-nvidia-bl-dkms (mbp_nvidia_bl) driver and is
generally preferred.


%package -n kernel%{_alt_kernel}-video-nvidiabl
Summary:	Linux driver for nVidia display back-lights
Summary(pl.UTF-8):	Sterownik dla Linuksa do nvidiabl
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-video-nvidiabl
This driver drives the smartdimmer register found on modern mobile
nVidia graphics adapters such as NV40, NV41, NV43, NV44, NV46, NV47,
NV49, NV4B, C51, G84, G86, G92, G94, G96, GT200 architectures to
adjust the display backlight.

On Apple machines this driver allows more fine-grained brightness
adjustment than the (mbp_nvidia_bl) driver and is generally preferred.

%description -n kernel%{_alt_kernel}-video-nvidiabl -l pl.UTF-8
Sterownik dla Linuksa do nvidiabl.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -qn %{modname}-%{version}
%patch0 -p1

%build
%if %{with kernel}
%build_kernel_modules -m nvidiabl
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with kernel}
%install_kernel_modules -m nvidiabl -d misc
install -d $RPM_BUILD_ROOT/etc/modprobe.d
cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/modprobe.d/%{modname}.conf
%endif

%if %{with dkms}
install -d $RPM_BUILD_ROOT%{_usrsrc}/%{modname}-%{version}-%{rel}
cp -p Makefile *.[ch] $RPM_BUILD_ROOT%{_usrsrc}/%{modname}-%{version}-%{rel}
sed -e 's|@MODNAME@|%{modname}|g' -e 's|@MODVERSION@|%{version}-%{rel}|g' \
	dkms.conf > $RPM_BUILD_ROOT%{_usrsrc}/%{modname}-%{version}-%{rel}/dkms.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n dkms-%{modname}
%{_sbindir}/dkms add -m %{modname} -v %{version}-%{rel} --rpm_safe_upgrade && \
%{_sbindir}/dkms build -m %{modname} -v %{version}-%{rel} --rpm_safe_upgrade && \
%{_sbindir}/dkms install -m %{modname} -v %{version}-%{rel} --rpm_safe_upgrade || :

%preun -n dkms-%{modname}
%{_sbindir}/dkms remove -m %{modname} -v %{version}-%{rel} --rpm_safe_upgrade --all || :

%post	-n kernel%{_alt_kernel}-video-nvidiabl
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-video-nvidiabl
%depmod %{_kernel_ver}

%if %{with dkms}
%files -n dkms-%{modname}
%defattr(644,root,root,755)
%{_usrsrc}/%{modname}-%{version}-%{rel}
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-video-nvidiabl
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
%config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/%{modname}.conf
%endif
