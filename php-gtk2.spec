%define snapshot 20130225

Summary:	GTK+2 toolkit for php
Name:		php-gtk2
Version:	2.0.3
Release:	0.svn%{snapshot}.4
Epoch:		2
License:	LGPLv2.1
Group:		Development/PHP
Url:		https://gtk.php.net/
Source0:	https://github.com/php/php-gtk-src/php-gtk2-%{version}-0.git%{snapshot}.tar.gz
Source1:	php_cairo_api.h
Patch0:		cairo_local_path.patch
Patch1:		php-gtk2-automake1.13.patch
Patch2:         php-gtk2-2.0.3-fix-php5.5.patch
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	php-mbstring
BuildRequires:	php-cairo
BuildRequires:	php-cli >= 3:5.3.0
Requires:	php-cli >= 3:5.3.0
Requires:	php-cairo

%description
PHP-GTK is an extension for PHP programming language that implements language
bindings for GTK+ toolkit. It provides an object-oriented interface to GTK+
classes and functions and greatly simplifies writing client side cross-platform
GUI applications.

%prep
%setup -q -n php-gtk2
%patch0 -p0
%patch1 -p1
%patch2 -p1

cp %{SOURCE1} main/php_cairo_api.h

for i in `find . -type d -name .git`; do
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
rm libtool
ln -s %{_bindir}/libtool libtool

sed -i.orig 's/compile $(CC)/compile --tag=CC $(CC)/g' Makefile
sed -i.orig 's/link $(CC)/link --tag=CC $(CC)/g' Makefile

make

%install
install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions

install -m0755 modules/php_gtk2.so %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/A99_gtk2.ini << EOF
extension = php_gtk2.so

[php-gtk]

;php-gtk.codepage = iso-8859-1
;php-gtk.extensions = 

EOF

%files
%doc demos AUTHORS ChangeLog NEWS README* TODO2
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*
%{_libdir}/php/extensions/php_gtk2.so

