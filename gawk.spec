Summary: The GNU version of the awk text processing utility.
Name: gawk
Version: 3.1.1
Release: 9
License: GPL
Group: Applications/Text
Source0: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}-ps.tar.gz
Patch0: gawk-3.1.0-newsecurity.patch
Patch1: gawk-3.1.0-shutup.patch
Patch2: gawk-3.1.1-ngroups.patch
Prereq: /sbin/install-info
Requires: /bin/mktemp
Buildroot: %{_tmppath}/%{name}-root

%description
The gawk packages contains the GNU version of awk, a text processing
utility. Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs.

Install the gawk package if you need a text processing utility. Gawk is
considered to be a standard Linux tool for processing text.

%prep
%setup -q -b 1
%patch0 -p1 -b .mktemp
%patch1 -p1
%patch2 -p1

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall bindir=${RPM_BUILD_ROOT}/bin \
	libexecdir=${RPM_BUILD_ROOT}%{_libexecdir}/awk \
	datadir=${RPM_BUILD_ROOT}%{_datadir}/awk

mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -sf gawk.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/awk.1.gz
ln -sf ../../bin/gawk $RPM_BUILD_ROOT%{_bindir}/awk
ln -sf ../../bin/gawk $RPM_BUILD_ROOT%{_bindir}/gawk
rm -f $RPM_BUILD_ROOT/bin/{,p}gawk-%{version}

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
mv -f $RPM_BUILD_ROOT%{_datadir}/awk/locale $RPM_BUILD_ROOT%{_datadir}/locale

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/gawk.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/gawk.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root,-)
%doc README COPYING FUTURES INSTALL LIMITATIONS NEWS
%doc README_d POSIX.STD doc/gawk.ps doc/awkcard.ps
/bin/*
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/gawk.info*
%{_libexecdir}/awk
%{_datadir}

%changelog
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

* Tue Aug 15 2000 Trond Eivind Glomsr�d <teg@redhat.com>
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

