# TODO:
# - add desktop and png icon for bins-edit-gui.
#
%include	/usr/lib/rpm/macros.perl
Summary:	HTML photo album generator
Summary(pl):	Generator albumów fotograficznych w HTML
Name:		bins
Version:	1.1.21
Release:	2
License:	GPL
Group:		Applications/Graphics
Source0:	http://jsautret.free.fr/BINS/%{name}-%{version}.tar.bz2
Patch0:		%{name}-localedir.patch
Patch1:		%{name}-gladedir.patch
URL:		http://bins.sautret.org/
Requires:	ImageMagick
BuildArch:	noarch
BuildRequires:	rpm-perlprov >= 3.0.3-18
%requires_eq	perl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
The aim of BINS is to generate static HTML photo albums.

%description -l pl
BINS s³u¿y do generowania albumów fotograficznych w postaci statyczych
stron HTML.

%package edit-gui
Summary:	Editor GUI for BINS
Summary(pl):	Interfejs u¿ytkownika do edycji albumów BINS
Group:		Applications/Graphics
Requires:	%{name} = %{version}

%description edit-gui
GUI for editing BINS albums.

%description edit-gui -l pl
Graficzny interfejs u¿ytkownika do edycji albumów BINS.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1} \
	   $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1} \
	   $RPM_BUILD_ROOT%{_datadir}/%{name} \
	   $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/templates.default \
	   $RPM_BUILD_ROOT%{_datadir}/locale/{fr,de,pl}/LC_MESSAGES

install bins bins_edit $RPM_BUILD_ROOT%{_bindir}
install bins-edit-gui $RPM_BUILD_ROOT%{_bindir}
install binsrc $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install templates/*.html $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/templates.default
install bins-edit-gui.glade $RPM_BUILD_ROOT%{_datadir}/%{name}
install doc/{bins,bins_edit}.1 $RPM_BUILD_ROOT%{_mandir}/man1
install doc/*gui*.1 $RPM_BUILD_ROOT%{_mandir}/man1

for L in fr de pl ; do
	install intl/$L.mo $RPM_BUILD_ROOT%{_datadir}/locale/$L/LC_MESSAGES/%{name}.mo
	if [ -f intl/gui-$L.mo ] ; then
		install intl/gui-$L.mo $RPM_BUILD_ROOT%{_datadir}/locale/$L/LC_MESSAGES/%{name}-edit-gui.mo
	fi
done

%find_lang %{name}
%find_lang %{name}-edit-gui

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CREDITS ChangeLog README TODO doc/*.html
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}/binsrc
%dir %{_sysconfdir}/%{name}/templates.default
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}/templates.default/*
%{_mandir}/man1/*

%files edit-gui -f %{name}-edit-gui.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bins-edit-gui
%{_mandir}/man1/*
%{_datadir}/%{name}
