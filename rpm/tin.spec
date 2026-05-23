Name: tin
Summary: An easy-to-use USENET news reader
Version: 2.6.5
%define srcversion 2.6.5
Release: 1
License: BSD
Group: Applications/News
## Source0: ftp://ftp.tin.org/pub/news/clients/tin/v2.6/%{name}-%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz
Source1: %{name}-%{version}.tar.bz2
## BuildRoot: %%{name}-%%{version}-%%{release}
#Packager: Dirk Nimmich <nimmich@muenster.de>
Packager: Peter Leinchen (for SFOS) <peterleinchen@t-online.de>

BuildRequires: pkgconfig(ncursesw)
#BuildRequires: pkgconfig(libressl) # not available in Jolla repo, but would be in nielnielsen
#BuildRequires: pkgconfig(openssl) # way too old in Jolla repo, 1.1.1
#BuildRequires: pkgconfig(gnutls) # too old in Jolla repo 2.12.24, but chum has 3.7
BuildRequires: pkgconfig(gnutls) >= 3.7.0
BuildRequires: bison byacc flex
BuildRequires: gettext
BuildRequires: pkgconfig(zlib)
# Not avalaible on OBS and NOT needed: BuildRequires: sb2 qemu-user

%define confdir /etc/tin
%global faqdir %{_datadir}/%{name}-%{version}/faq


%description
An easy-to-use USENET news reader for the console using NNTP.
It supports threading, scoring, different charsets, and many other
useful things. It has also support for different languages.


%package doc
Summary:    Documentation, FAQ, and manuals for the tin news reader
Group:      Documentation
Requires:   %{name} = %{version}-%{release}


%description doc
This package contains the text manuals, comprehensive FAQ logs, sample layouts, 
and system man pages for the tin news reader.


%prep
%setup -q -a 1
## moved to build
##CFLAGS="$RPM_OPT_FLAGS" ./configure...


%build
# This ensures YACC, LEX, and CC are mapped correctly for cross-compiling. With %%configure
# Force the paths to the host tools to bypass sb2's detection failure
export YACC=/usr/bin/yacc
export LEX=/usr/bin/flex

# Use the macro instead of calling ./configure manually. NOT important
##CFLAGS="$RPM_OPT_FLAGS" ./configure...
#CFLAGS="$RPM_OPT_FLAGS" %%configure...

#export CFLAGS="$RPM_OPT_FLAGS"
#export CPPFLAGS="$RPM_OPT_FLAGS"
#export LDFLAGS="$RPM_OPT_FLAGS"
#export LANG=C.UTF-8
#export LC_ALL=C.UTF-8

CFLAGS="%{optflags}" \
CPPFLAGS="%{optflags}" \
LDFLAGS="%{optflags}" \
%configure \
 --sysconfdir=%{confdir} \
 --verbose \
 --disable-echo \
 --enable-prototypes \
 --enable-nntp-only \
 --with-nntps \
 --enable-cancel-locks \
 --enable-long-article-numbers \
 --with-pcre2-config \
 --with-screen=ncursesw

## make build
# Use the macro for make to benefit from parallel building
## %%make_build build
%make_build


%install
## make install
## make install_sysdefs
# Use DESTDIR for the buildroot instead of --with-install-prefix
%make_install
make DESTDIR=%{buildroot} install_sysdefs
mkdir -p %{buildroot}/%{faqdir}
cp %{name}-%{srcversion}/faq/* %{buildroot}/%{faqdir}/


%files
%dir %attr(755,root,root) %{confdir}
%config(noreplace) %attr(644,root,root) %{confdir}/*
%{_bindir}/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%doc README
%dir %{_datadir}/%{name}-%{version}
%dir %{faqdir}
%{faqdir}/*


%files doc
%defattr(-,root,root,-)
%{_mandir}/man1/*
%{_mandir}/man5/*
%doc doc/CHANGES doc/CHANGES.old doc/INSTALL doc/TODO doc/WHATSNEW
%doc doc/auth.txt doc/filtering doc/good-netkeeping-seal doc/iso2asc.txt
%doc doc/keymap.sample doc/mailcap.sample doc/mime.types doc/tin.defaults
%doc doc/pgp.txt doc/reading-mail.txt
%doc doc/tools.txt doc/umlaute.txt doc/umlauts.txt
%doc doc/wildmat.3
%doc doc/article.txt doc/art_handling.txt doc/internals.txt doc/rcvars.txt
%doc doc/config-anomalies doc/nov_tests doc/DEBUG_REFS
%doc doc/CREDITS


%post
# Inside post, pre, preun, postun scriptlets, comments do NOT protect macro expansion. And escaping with double PERCENT does also not work.
# { [ -d /home/nemo ] && ln -sf PERCENT{faqdir} /home/nemo/Documents/tin.faq; } || { [ -d /home/defaultuser ] && ln -sf PERCENT{faqdir} /home/defaultuser/Documents/tin.faq; }
if [ -d /home/nemo ]; then
    echo "ln -sf %{faqdir} /home/nemo/Documents/tin.faq" | su - nemo
elif [ -d /home/defaultuser ]; then
    echo "ln -sf %{faqdir} /home/defaultuser/Documents/tin.faq" | su - defaultuser
fi


%preun
if [ "$1" -eq 0 ]; then
    # { [ -L /home/nemo/Documents/tin.faq ] && rm /home/nemo/Documents/tin.faq; } || { [ -L /home/defaultuser/Documents/tin.faq ] && rm /home/defaultuser/Documents/tin.faq; }
    if [ -L /home/nemo/Documents/tin.faq ]; then
        rm /home/nemo/Documents/tin.faq
    elif [ -L /home/defaultuser/Documents/tin.faq ]; then
        rm /home/defaultuser/Documents/tin.faq
    fi
fi


%changelog
* Mon May 18 2026 Peter Leinchen <peterleinchen@t-online.de>
- Isolated documentation payload, man pages, and the text FAQ folder into a separate doc package for SFOS.

* Fri May 08 2026 Peter Leinchen <peterleinchen@t-online.de>
  Specfile created for tin 2.6.5 on SFOS.
#
#× Tue Jul 22 2003 Dirk Nimmich <nimmich@muenster.de>
#  Specfile created for tin 1.6.0.