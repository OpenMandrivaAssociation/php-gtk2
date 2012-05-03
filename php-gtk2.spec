%define _requires_exceptions pear(EventGenerator.config.php)\\|pear(bugconfig.php)

%define snapshot 305683
%define rel 10
%if %snapshot
%define release %mkrel 0.svn%snapshot.%rel
%else
%define release %mkrel %rel
%endif

Summary:	GTK+2 toolkit for php
Name:		php-gtk2
Version:	2.0.3
Release:	%release
Group:		Development/PHP
License:	LGPLv2.1
URL:		http://gtk.php.net/
Source0:	http://gtk.php.net/distributions/php-gtk2-%{version}-0.svn%{snapshot}.tar.gz
Source1:	php_cairo_api.h
Patch0:		php-gtk-2.0.2-make-3.8.patch
Patch1:		cairo_local_path.patch
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	glib2-devel >= 2.6.0
BuildRequires:	gtk+2-devel >= 2.6.9
BuildRequires:	libpango-devel >= 1.8.0
BuildRequires:	php-mbstring
BuildRequires:	libglade2.0-devel >= 2.4.0
BuildRequires:	php-cairo
BuildRequires:	php-cli >= 3:5.3.0
Requires:	php-cli >= 3:5.3.0
Conflicts:	apache-mod_php
Epoch:		2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PHP-GTK is an extension for PHP programming language that implements language
bindings for GTK+ toolkit. It provides an object-oriented interface to GTK+
classes and functions and greatly simplifies writing client side cross-platform
GUI applications.

%prep
%setup -q -n php-gtk2
%patch0 -p0
%patch1 -p0

cp %{SOURCE1} main/php_cairo_api.h

for i in `find . -type d -name .svn`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%build
%serverbuild
rm -f configure
rm -rf autom4te.cache
./buildconf

%configure2_5x \
    --with-libdir=%{_lib}

# We use our own libtool, and apply some fixes
%{__rm} libtool
ln -s %{_bindir}/libtool libtool

sed -i.orig 's/compile $(CC)/compile --tag=CC $(CC)/g' Makefile
sed -i.orig 's/link $(CC)/link --tag=CC $(CC)/g' Makefile

# link some files in order to have enough gtk support for not released yet 2.19 gtk
pushd ext/gtk+/
ln -s gtk-2.18.defs gtk-2.19.defs
ln -s gtk-2.18.overrides gtk-2.19.overrides
ln -s gtk-2.18-types.defs gtk-2.19-types.defs
popd

make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions

install -m0755 modules/php_gtk2.so %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/A99_gtk2.ini << EOF
extension = php_gtk2.so

[php-gtk]

;php-gtk.codepage = iso-8859-1
;php-gtk.extensions = 

EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc demos test AUTHORS ChangeLog NEWS README* TODO2
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*
%{_libdir}/php/extensions/php_gtk2.so
