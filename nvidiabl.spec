#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		rel	2
%define		pname	nvidiabl
Summary:	Linux driver for nVidia display back-lights
Name:		%{pname}%{_alt_kernel}
Version:	0.81
Release:	%{rel}
License:	GPL v2+
URL:		https://github.com/guillaumezin/nvidiabl
Source0:	https://github.com/guillaumezin/nvidiabl/archive/v%{version}.tar.gz?/%{pname}-%{version}.tgz
# Source0-md5:	f72d90c0fe34b36a0ff3b6d7034e99c4
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
%setup -qn %{pname}-%{version}

%build
%build_kernel_modules -m nvidiabl

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m nvidiabl -d misc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-video-nvidiabl
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-video-nvidiabl
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-video-nvidiabl
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
