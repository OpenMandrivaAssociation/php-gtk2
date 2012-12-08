#define _requires_exceptions pear(EventGenerator.config.php)\\|pear(bugconfig.php)

%define snapshot 20120905
%define rel 1

%if %{snapshot}
%define release 0.svn%{snapshot}.%{rel}
%else
%define release %{rel}
%endif

Summary:	GTK+2 toolkit for php
Name:		php-gtk2
Version:	2.0.3
Release:	%{release}
Epoch:		2
Group:		Development/PHP
License:	LGPLv2.1
URL:		http://gtk.php.net/
# Now it's in git: http://git.php.net/?p=php/gtk-src.git
Source0:	php-gtk2-%{version}-0.svn%{snapshot}.tar.gz
Source1:	php_cairo_api.h
Patch1:		cairo_local_path.patch
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	php-mbstring
BuildRequires:	pkgconfig(libglade-2.0) >= 2.4.0
BuildRequires:	php-cairo
BuildRequires:	php-cli >= 3:5.3.0
Requires:	php-cli >= 3:5.3.0
Conflicts:	apache-mod_php

%description
PHP-GTK is an extension for PHP programming language that implements language
bindings for GTK+ toolkit. It provides an object-oriented interface to GTK+
classes and functions and greatly simplifies writing client side cross-platform
GUI applications.

%prep
%setup -q -n php-gtk2
%patch1 -p0

cp %{SOURCE1} main/php_cairo_api.h

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

%files
%doc demos AUTHORS ChangeLog NEWS README* TODO2
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*
%{_libdir}/php/extensions/php_gtk2.so


%changelog
* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.3-0.svn305683.8mdv2011.0
+ Revision: 696428
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.3-0.svn305683.7
+ Revision: 695403
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.3-0.svn305683.6
+ Revision: 646647
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.3-0.svn305683.5mdv2011.0
+ Revision: 629809
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.3-0.svn305683.4mdv2011.0
+ Revision: 628108
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.3-0.svn305683.3mdv2011.0
+ Revision: 600494
- rebuild

* Tue Nov 23 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.3-0.svn305683.2mdv2011.0
+ Revision: 599915
- fix #61758 (undefined symbol (php-gtk2))
- 2.0.3 (r305683)
- better logic for local php_cairo_api.h

* Mon Oct 25 2010 Funda Wang <fwang@mandriva.org> 2:2.0.2-0.svn289364.4mdv2011.0
+ Revision: 589225
- fix build with newer make

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.2-0.svn289364.2mdv2010.1
+ Revision: 514551
- rebuilt for php-5.3.2

* Thu Jan 28 2010 Stéphane Téletchéa <steletch@mandriva.org> 2:2.0.2-0.svn289364.1mdv2010.1
+ Revision: 497836
- Incorporate the php_cairo api file inside the spec to have a 'portable' solution
- Adjust naming for bs
- Update to lastest snapshot instead of waiting for a putative release
- Drop patches since they are already applied
- Link 2.18 definitions to 2.19 since otherwise we will miss some gtk definitions
- Remove svn dirs also (the project is managed under svn now)
- Adjust LGPL version

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.1-14mdv2010.1
+ Revision: 485367
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.1-13mdv2010.1
+ Revision: 468172
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.1-12mdv2010.0
+ Revision: 451276
- rebuild

* Mon Sep 28 2009 Stéphane Téletchéa <steletch@mandriva.org> 2:2.0.1-11mdv2010.0
+ Revision: 450625
- no BR on php-sqlite since it is bundled by default in php 5.3
- Rebuild against 5.3.1RC1
- Remove libglade configure option as it is not recognised
- Add missing BR

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Raphaël Gertz <rapsys@mandriva.org>
    - Rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.1-6mdv2009.1
+ Revision: 346475
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.1-5mdv2009.1
+ Revision: 341753
- rebuilt against php-5.2.9RC2

* Sun Jan 04 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.1-4mdv2009.1
+ Revision: 324395
- fix build with -Werror=format-security

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.1-3mdv2009.1
+ Revision: 310272
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.1-2mdv2009.0
+ Revision: 238399
- rebuild

* Tue May 20 2008 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.1-1mdv2009.0
+ Revision: 209367
- 2.0.1
- make it conflict with apache-mod_php (http://gtk.php.net/faq.php#2)

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-1.beta.5mdv2008.1
+ Revision: 162226
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-1.beta.4mdv2008.1
+ Revision: 107641
- restart apache if needed

* Thu Nov 08 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-1.beta.3mdv2008.1
+ Revision: 106870
- fix #35406 (php-gtk2 example files link to wrong module)

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-1.beta.2mdv2008.0
+ Revision: 77546
- rebuilt against php-5.2.4

* Fri Jul 13 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-1.beta.1mdv2008.0
+ Revision: 51852
- 2.0.0beta
- use the %%serverbuild macro

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-1.alpha.6mdv2008.0
+ Revision: 39498
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-1.alpha.5mdv2008.0
+ Revision: 33809
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-1.alpha.4mdv2008.0
+ Revision: 21331
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-1.alpha.3mdv2007.0
+ Revision: 117586
- rebuilt against new upstream version (5.2.1)

* Mon Nov 20 2006 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-1.alpha.2mdv2007.1
+ Revision: 85472
- rebuild
- rebuild
- use the official release for php-5.2.0
- rebuild
- rebuild
- rebuilt for php-5.2.0
- Import php-gtk2

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-0.20051124.1
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-1.20051124.4mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-0.20051124.4mdk
- rebuilt for php-5.1.3

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-0.20051124.3mdk
- rebuilt against php-5.1.2

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-0.20051124.2mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-0.20051124.1mdk
- new snap (20051124)
- drop upstream patch P0
- rebuilt against php-5.1.0
- fix versioning

* Mon Oct 03 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_2.0.0-0.20050921.2mdk
- filter out some pear stuff

* Sun Oct 02 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_2.0.0-0.20050921.1mdk
- initial Mandriav package

