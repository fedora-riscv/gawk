%define enable_japanese 1

Summary: The GNU version of the awk text processing utility.
Name: gawk
Version: 3.0.4
Release: 2j3
Copyright: GPL
Group: Applications/Text
Source0: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}-ps.tar.gz
Patch: gawk-3.0-unaligned.patch
Patch10: http://member.nifty.ne.jp/wills/program/gawkmb113.diff.gz
Prereq: /sbin/install-info
BuildRoot: /var/tmp/%{name}-root

%description
The gawk packages contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs.

Install the gawk package if you need a text processing utility. Gawk is
considered to be a standard Linux tool for processing text.

%prep
%setup -q -b 1
%patch -p1
%if %{enable_japanese}
%patch10 -p1
%endif

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall mandir=${RPM_BUILD_ROOT}%{_mandir}/man1 \
        bindir=${RPM_BUILD_ROOT}/bin \
        libexecdir=${RPM_BUILD_ROOT}%{_libexecdir}/awk \
        datadir=${RPM_BUILD_ROOT}%{_datadir}/awk
#make install prefix=$RPM_BUILD_ROOT%{_prefix} bindir=$RPM_BUILD_ROOT/bin libexedir=$RPM_BUILD_ROOT/libexec
#strip ${RPM_BUILD_ROOT}/bin/gawk || :
#strip ${RPM_BUILD_ROOT}%{_prefix}/libexec/awk/* || :

( cd $RPM_BUILD_ROOT
  rm -f .%{_infodir}/dir
  gzip -9nf .%{_infodir}/gawk.info*
  mkdir -p .%{_prefix}/bin
  cd .%{_mandir}/man1
  ln -sf gawk.1.gz awk.1.gz
  cd $RPM_BUILD_ROOT
  ln -sf /bin/gawk .%{_prefix}/bin/awk
  ln -sf /bin/gawk .%{_prefix}/bin/gawk
)

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/gawk.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/gawk.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc README COPYING ACKNOWLEDGMENT FUTURES INSTALL LIMITATIONS NEWS PORTS 
%doc README_d POSIX.STD doc/gawk.ps doc/awkcard.ps
/bin/*
%{_prefix}/bin/*
%{_mandir}/man1/*
%{_infodir}/gawk.info*
%{_prefix}/libexec/awk
%{_prefix}/share/awk

%changelog
* Mon Sep 11 2000 Matt Wilson <msw@redhat.com>
- added %%defattr(-,root,root)

* Tue Aug 01 2000 Yukihiro Nakai <ynakai@redhat.com>
- Update japanese patch to 2000.06.18 version.
- Rebuild for 7.0J

* Wed Mar 15 2000 Matt Wilson <msw@redhat.com>
- use enable_japanese macro

* Tue Mar 14 2000 Chris Ding <cding@redhat.com>
- added patch for multi-byte

* Thu Feb  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix man page symlinks
- Fix description
- Fix download URL

* Wed Jun 30 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.0.4.

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- make sure all binaries are stripped

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Fri Feb 19 1999 Jeff Johnson <jbj@redhat.com>
- Install info pages (#1242).

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1
- don't package /usr/info/dir

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 3.0.3
- added documentation and buildroot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

