Summary: The GNU version of the awk text processing utility.
Name: gawk
Version: 3.1.5
Release: 9
License: GPL
Group: Applications/Text
Source0: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}-ps.tar.gz
Prereq: /sbin/install-info
Requires: /bin/mktemp
Buildroot: %{_tmppath}/%{name}-root

BuildRequires: flex
BuildRequires: bison

Patch1: gawk-3.1.3-getpgrp_void.patch
Patch2: gawk-3.1.5-free.patch
Patch3: gawk-3.1.5-fieldwidths.patch
Patch4:	gawk-3.1.5-binmode.patch
Patch5: gawk-3.1.5-num2str.patch
Patch6: gawk-3.1.5-wconcat.patch
#  fix internal names like /dev/user, /dev/pid, as well as /dev/fd/N
Patch7: gawk-3.1.5-internal.patch
# 194214 - gawk coredumps on syntax error
Patch8: gawk-3.1.5-syntaxerror.patch
# http://lists.gnu.org/archive/html/bug-gnu-utils/2006-07/msg00004.html
Patch9: gawk-3.1.5-numflags.patch

%description
The gawk packages contains the GNU version of awk, a text processing
utility. Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs.

Install the gawk package if you need a text processing utility. Gawk is
considered to be a standard Linux tool for processing text.

%prep
%setup -q -b 1
%patch1 -p1 -b .getpgrp_void
%patch2 -p1 -b .free
%patch3 -p1 -b .fieldwidths
%patch4 -p1 -b .binmode
%patch5 -p1 -b .num2str
%patch6 -p1 -b .wconcat
%patch7 -p1 -b .internal
%patch8 -p1 -b .syntaxerror

%build
%configure
make
make check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall bindir=${RPM_BUILD_ROOT}/bin \
	libexecdir=${RPM_BUILD_ROOT}%{_libexecdir} \
	datadir=${RPM_BUILD_ROOT}%{_datadir}

mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -sf gawk.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/awk.1.gz
ln -sf ../../bin/gawk $RPM_BUILD_ROOT%{_bindir}/awk
ln -sf ../../bin/gawk $RPM_BUILD_ROOT%{_bindir}/gawk
rm -f $RPM_BUILD_ROOT/bin/{,p}gawk-%{version}

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_infodir}/gawk.info.gz ]; then
    /sbin/install-info %{_infodir}/gawk.info.gz %{_infodir}/dir
fi

%preun
if [ $1 = 0 -a -f %{_infodir}/gawk.info.gz ]; then
   /sbin/install-info --delete %{_infodir}/gawk.info.gz %{_infodir}/dir
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING FUTURES LIMITATIONS NEWS
%doc README_d POSIX.STD doc/gawk.ps doc/awkcard.ps
/bin/*
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/gawk.info*
%{_infodir}/gawkinet.info*
%{_libexecdir}/awk
%{_datadir}/awk

%changelog
* Mon Jul 10 2006 Karel Zak <kzak@redhat.com> 3.1.5-9
- fix numeric conversion problem (patch by Aharon Robbins)
  http://lists.gnu.org/archive/html/bug-gnu-utils/2006-07/msg00004.html

* Fri Jun 23 2006 Karel Zak <kzak@redhat.com> 3.1.5-8
- fix #194214 - gawk coredumps on syntax error (patch by Aharon Robbins)

* Wed Jun 21 2006 Karel Zak <kzak@redhat.com> 3.1.5-7
- fix internal names like /dev/user, /dev/pid, or /dev/fd/N (patch by Aharon Robbins)

* Tue Feb 14 2006 Karel Zak <kzak@redhat.com> 3.1.5-6.2
- new version of the gawk-3.1.5-wconcat.patch patch

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.1.5-6.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Karel Zak <kzak@redhat.com> 3.1.5-6
- fix wide characters concatenation

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.1.5-5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Dec 22 2005 Karel Zak <kzak@redhat.com> 3.1.5-5
- fix "gawk -v BINMODE=1" (patch by Aharon Robbins)
- fix conversion from large number to string (patch by Aharon Robbins)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Oct  9 2005 Karel Zak <kzak@redhat.com> 3.1.5-4
- fix off-by-one error in assignment of sentinel value at 
  end of FIELDWIDTHS array. (patch by Aharon Robbins)

* Tue Sep 27 2005 Karel Zak <kzak@redhat.com> 3.1.5-3
- fix #169374 - Invalid Free (patch by Aharon Robbins)

* Tue Sep 20 2005 Karel Zak <kzak@redhat.com> 3.1.5-2
- fix #167181 - gawk owns /usr/share
- fix #160634 - should exclude dirs in spec file

* Tue Sep 20 2005 Karel Zak <kzak@redhat.com> 3.1.5-1
- new upstream version

* Wed Jun 15 2005 Karel Zak <kzak@redhat.com> 3.1.4-6
- fix #160421 - crash when using non-decimal data in command line parameters

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 3.1.4-5
- rebuild with gcc-4

* Fri Nov 12 2004 Karel Zak <kzak@redhat.com> 3.1.4-4
- rebuilt 

* Thu Nov 11 2004 Karel Zak <kzak@redhat.com> 3.1.4-3
- rebuilt to FC4 

* Tue Nov  9 2004 Karel Zak <kzak@redhat.com> 3.1.4-2
- add dfacache.patch for fix LC_ALL=de_DE.UTF-8 ./gawk '/^[ \t]/ { print }',
  (by Aharon Robbins), #135210, #131498
- add flonum.patch for "improved" handling of non-numeric constants,
  second version of patch (by Aharon Robbins)
  http://lists.gnu.org/archive/html/bug-gnu-utils/2004-10/msg00046.html
- add nextc.patch (by Andreas Schwab)
  http://lists.gnu.org/archive/html/bug-gnu-utils/2004-09/msg00093.html
- add uplow.patch for fix the wide char handling (by Stepan Kasal)
  http://lists.gnu.org/archive/html/bug-gnu-utils/2004-10/msg00099.html

* Tue Aug 31 2004 Thomas Woerner <twoerner@redhat.com> 3.1.4-1
- new version 3.1.4

* Mon Jun 28 2004 Thomas Woerner <twoerner@redhat.com> 3.1.3-9
- fixed "read only one input file on 64-bit architectures"

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Thomas Woerner <twoerner@redhat.com> 3.1.3-6
- fixed getpgrp_void problem (#114246)
- removed old patches

* Fri Jan 09 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- add a "make check"

* Mon Dec 08 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- disabled "shutup" patch to warn about wrong awk scripts again

* Mon Sep 22 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add even more patches from the mailinglist

* Tue Jul 15 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add first bug-fixes from the mailinglist

* Sun Jul 13 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.1.3
- pgawk man-page fix and /proc fix are obsolete

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix --exclude-docs #92252

* Sun May 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix find_lang

* Tue Apr 15 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix .so pointer in pgawk man-page
- also read files in /proc correctly that have a filesize of 0

* Sun Mar 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.1.2

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec 02 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add find_lang to specfile

* Wed Nov 20 2002 Elliot Lee <sopwith@redhat.com> 3.1.1-7
- Add gawk-3.1.1-ngroups.patch, because NGROUPS_MAX comes from 
sys/param.h, and awk.h changes behaviour depending on whether NGROUPS_MAX 
is defined or not. (For ppc64)

* Wed Nov 06 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- remove /usr/share/info/dir

* Sun Nov 03 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- ugly fix to get locale files into the right location #74360

* Sun Aug 11 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- simplify install part of spec file
- do not package /bin/gawk-<version>  anymore

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 09 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.1.1

* Sun Mar 17 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add patch from #61316 to ignore wrong hex numbers and treat them as text

* Tue Jul 31 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- do not warn about unnecessary escaping

* Fri Jun 29 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix path of man-pages

* Mon Jun 25 2001 Than Ngo <than@redhat.com> 3.1.0-1
- update to 3.1.0
- remove a uneeded patch
- adapt a patch for 3.1.0

* Fri Jun  1 2001 Preston Brown <pbrown@redhat.com>
- newer version of the mktemp patch from Solar Designer <solar@openwall.com>

* Fri May 11 2001 Preston Brown <pbrown@redhat.com> 3.0.6-2
- use mktemp in igawk shell script, not shell pid variable

* Wed Aug 16 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.06

* Tue Aug 15 2000 Trond Eivind Glomsrod <teg@redhat.com>
- /usr/bin/gawk can't point at gawk - infinite symlink
- /usr/bin/awk can't point at gawk - infinite symlink

* Mon Aug 14 2000 Preston Brown <pbrown@redhat.com>
- absolute --> relative symlinks

* Tue Aug  8 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- fix paths for "configure" call

* Thu Jul 13 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- add another bugfix

* Thu Jul 13 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.0.5 with bugfix

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 30 2000 Matt Wilson <msw@redhat.com>
- revert to 3.0.4.  3.0.5 misgenerates e2fsprogs' test cases

* Wed Jun 28 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.0.5

* Mon Jun 19 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- add defattr

* Mon Jun 19 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- FHS

* Tue Mar 14 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- add bug-fix

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

