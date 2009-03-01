%define _requires_exceptions pear(EventGenerator.config.php)\\|pear(bugconfig.php)

Summary:	GTK+2 toolkit for php
Name:		php-gtk2
Version:	2.0.1
Release:	%mkrel 6
Group:		Development/PHP
License:	LGPL
URL:		http://gtk.php.net/
Source0:	http://gtk.php.net/distributions/php-gtk-%{version}.tar.gz
Patch0:		php-gtk-bug35406.diff
Patch1:		php-gtk-2.0.1-format_not_a_string_literal_and_no_format_arguments.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	glib2-devel >= 2.6.0
BuildRequires:	gtk+2-devel >= 2.6.9
BuildRequires:	libpango-devel >= 1.8.0
#BuildRequires:	libglade2.0-devel >= 2.4.0
BuildRequires:	php-cli >= 3:5.2.0
Requires:	php-cli >= 3:5.2.0
Conflicts:	apache-mod_php
Epoch:		2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PHP-GTK is an extension for PHP programming language that implements language
bindings for GTK+ toolkit. It provides an object-oriented interface to GTK+
classes and functions and greatly simplifies writing client side cross-platform
GUI applications.

%prep

%setup -q -n php-gtk-%{version}
%patch0 -p1
%patch1 -p0

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;
		
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%build
%serverbuild

./buildconf

%configure2_5x \
    --with-libdir=%{_lib} \
    --disable-libglade
  
make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions

install -m0755 modules/php_gtk2.so %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/60_php-gtk2.ini << EOF

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
