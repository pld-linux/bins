# TODO:
# - add desktop and png icon for bins-edit-gui.
#
%include	/usr/lib/rpm/macros.perl
Summary:	HTML photo album generator
Summary(pl):	Generator albumów fotograficznych w HTML-u
Name:		bins
Version:	1.1.26
Release:	1
License:	GPL
Group:		Applications/Graphics
Source0:	http://jsautret.free.fr/BINS/%{name}-%{version}.tar.bz2
# Source0-md5:	b260838a854557781e23b43e64c06f6b
Patch0:		%{name}-localedir.patch
Patch1:		%{name}-gladedir.patch
Patch2:		%{name}-datadir.patch
Patch3:		%{name}-po.patch
URL:		http://bins.sautret.org/
BuildRequires:	rpm-perlprov >= 3.0.3-18
Requires:	ImageMagick
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The aim of BINS is to generate static HTML photo albums.

%description -l pl
BINS s³u¿y do generowania albumów fotograficznych w postaci statycznych
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
%patch2 -p1
%patch3 -p1

# outdated
rm -f intl/zh_TW.Big5.po
rm -f intl/*.mo
# current
mv -f intl/zh{,_TW}.po
mv -f intl/messages.po{,t}
mv -f intl/bins-edit-gui.po{,t}

%build
cd intl
for L in *.po ; do
	msgfmt -o `basename $L .po`.mo $L
done
cd -

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	   $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1} \
	   $RPM_BUILD_ROOT%{_datadir}/%{name}

install anti_bins bins bins_edit $RPM_BUILD_ROOT%{_bindir}
install bins_cleanupgallery $RPM_BUILD_ROOT%{_bindir}
install bins-edit-gui $RPM_BUILD_ROOT%{_bindir}
install binsrc $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -r templates* $RPM_BUILD_ROOT%{_datadir}/%{name}
install bins-edit-gui.glade $RPM_BUILD_ROOT%{_datadir}/%{name}
install doc/{bins,bins_edit}.1 $RPM_BUILD_ROOT%{_mandir}/man1
install doc/*gui*.1 $RPM_BUILD_ROOT%{_mandir}/man1

cd intl
for L in ??.mo ??_??.mo ; do
	LL=`basename $L .mo`
	install -d $RPM_BUILD_ROOT%{_datadir}/locale/$LL/LC_MESSAGES
	install $LL.mo $RPM_BUILD_ROOT%{_datadir}/locale/$LL/LC_MESSAGES/%{name}.mo
	if [ -f gui-$LL.mo ] ; then
		install gui-$LL.mo $RPM_BUILD_ROOT%{_datadir}/locale/$LL/LC_MESSAGES/%{name}-edit-gui.mo
	fi
done
cd -

%find_lang %{name}
# The only file here is empty...
#%%find_lang %{name}-edit-gui

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CREDITS ChangeLog README TODO doc/*.html
%attr(755,root,root) %{_bindir}/bins
%attr(755,root,root) %{_bindir}/bins_edit
%attr(755,root,root) %{_bindir}/bins_cleanupgallery
%attr(755,root,root) %{_bindir}/anti_bins
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}/binsrc
%dir %{_datadir}/%{name}
%config(noreplace) %verify(not md5 size mtime) %{_datadir}/%{name}/templates*
%{_mandir}/man1/bins.1*
%{_mandir}/man1/bins_edit.1*

%files edit-gui
# -f %{name}-edit-gui.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bins-edit-gui
%{_mandir}/man1/bins-edit-gui.1*
%{_datadir}/%{name}
