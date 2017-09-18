#
# Important notes regarding the package:
# ======================================
#
# LICENSES: There are more licenses used inside the gawk source tarball from
#           upstream than listed in License: field below. However, some of
#           those files with different license are not used for compiling the
#           resulting binaries, nor they are additinionally shipped inside the
#           final package or its subpacakges
#
#           To get latest version of currently used licenses in gawk run the
#           licensecheck. We assume that files that do not explicitly state
#           their copyright are licensed under GPLv3+ as per COPYING file
#           inside root directory of source code.
#
#           Also, we have to ship additional license files with the package,
#           because upstream does not include them inside their source tarball:
#           and never will. They have also confirmed that the additional
#           licenses shipped are correct. For more info, see:
#
#           http://lists.gnu.org/archive/html/bug-gawk/2016-09/msg00008.html

# === GLOBAL MACROS ===========================================================

# According to Fedora Package Guidelines, it is advised that packages that can
# process untrusted input are build with position-idenpendent code (PIC).
#
# Koji should override the compilation flags and add the -fPIC or -fPIE flags by
# default. This is here just in case this wouldn't happen for some reason.
# For more info: https://fedoraproject.org/wiki/Packaging:Guidelines#PIE
%global _hardened_build 1

# We are defining the gawk(abi) version value based on these values, because
# upstream updates the API from time to time, which breaks the ABI for packages
# depending on gawk's shared objects. The gawk(abi) version value is exported
# below via the Provides: field.
#
# These values are defined in the gawkapi.h header file. To see them, run:
#   grep -E "gawk_api_(major|minor).*[[:digit:]]" gawkapi.h
%global gawk_api_major 1
%global gawk_api_minor 1

# =============================================================================

Name:             gawk
Summary:          The GNU version of the AWK text processing utility
Version:          4.1.4
Release:          7%{?dist}

License:          GPLv3+ and GPLv2+ and LGPLv2+ and BSD

URL:              https://www.gnu.org/software/gawk/
Source0:          https://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.xz

Source1:          LICENSE.GPLv2
Source2:          LICENSE.LGPLv2
Source3:          LICENSE.BSD

Provides:         /bin/awk
Provides:         /bin/gawk

Provides:         gawk(abi) = %{gawk_api_major}.%{gawk_api_minor}

# Safeguard to allow this package to be installed only on UsrMove enabled
# filesystem. More info: https://fedoraproject.org/wiki/Features/UsrMove
Requires:         filesystem >= 3
Requires(post):   info
Requires(preun):  info

BuildRequires:    ghostscript-core
BuildRequires:    git

# Extending GAWK possibilities:
BuildRequires:    libsigsegv-devel
BuildRequires:    mpfr-devel
BuildRequires:    readline-devel

# Documentation (gawk-doc):
BuildRequires:    texinfo-tex
BuildRequires:    texlive-ec
BuildRequires:    texlive-cm-super

# NOTE: In case any patch updates the awkgram.y or command.y (IOW if anything
#       changes the timestamp of awkgram.y, and it becomes newer than awkgram.c,
#       same applies for command.y), the 'make' command will automatically try
#       to rebuild the affected files. In that case we need to include the
#       BuildRequires line below.
#
# INFO: Upstream explicitly wishes that we do not use 'yacc' instead of bison.
#       For more info, see: https://bugzilla.redhat.com/show_bug.cgi?id=1176993
#BuildRequires:    bison

# =============================================================================

# NOTE: 'autosetup' macro (below) uses 'git' for applying the patches:
#       ->> All the patches should be provided in 'git format-patch' format.
#       ->> Auxiliary repository will be created during 'fedpkg prep', you
#           can see all the applied patches there via 'git log'.

# Upstream patches -- official upstream patches released by upstream since the
# ----------------    last rebase that are necessary for any reason:
Patch000: gawk-4.1.4-000-info-pages-fixes.patch


# Downstream patches -- these should be always included when doing rebase:
# ------------------
#Patch100: example100.patch


# Downstream patches for RHEL -- patches that we keep only in RHEL for various
# ---------------------------    reasons, but are not enabled in Fedora:
%if %{defined rhel} || %{defined centos}
#Patch200: example200.patch
%endif


# Patches to be removed -- deprecated functionality which shall be removed at
# ---------------------    some point in the future:


%description
The gawk package contains the GNU version of AWK text processing utility. AWK is
a programming language designed for text processing and typically used as a data
extraction and reporting tool.

The gawk utility can be used to do quick and easy text pattern matching,
extracting or reformatting. It is considered to be a standard Linux tool for
text processing.

# === SUBPACKAGES =============================================================

%package devel
Summary:          Header file for gawk extensions development
Requires:         %{name} = %{version}-%{release}
BuildArch:        noarch

%description devel
This subpackage provides /usr/include/gawkapi.h header file, which contains
definitions for use by extension functions calling into gawk. For more info
about gawk extensions, please refer to `The GNU Awk User's Guide`.

However, unless you are developing an extension to gawk, you most likely do not
need this subpackage.

# ---------------

%package doc
Summary:          Additional documentation for gawk utility
Requires:         %{name} = %{version}-%{release}
BuildArch:        noarch

%description doc
The base package of gawk comes pre-installed with `GAWK: Effective AWK
Programming` and `TCP/IP Internetworking with gawk` user's guides, and you can
access them via info pages.

However, this way of displaying information is less convenient for printing or
displaying images. Therefore, this doc subpackage can provide you with HTML, PDF
and PS versions of those documents, which might be useful when you need to
access them regularly, and/or when you do not have access to Internet.

# === BUILD INSTRUCTIONS ======================================================

# Call the 'autosetup' macro to prepare the environment, but do not patch the
# source code yet -- we need to copy the LICENSE.* files into the directory:
%prep
%autosetup -N -S git
cp -a %{SOURCE1} %{SOURCE2} %{SOURCE3} .

# Add and amend the copied files to the initial commit, patch the source code:
git add --all --force .
git commit --all --amend --no-edit > /dev/null
%autopatch -p1

# ---------------

%build
%configure
make %{?_smp_mflags}

# Build the documentation in PDF, postscript and HTML versions:
make -C doc pdf
mkdir -p html/gawk html/gawkinet
makeinfo --html -I doc -o html/gawk     doc/gawk.texi
makeinfo --html -I doc -o html/gawkinet doc/gawkinet.texi

# ---------------

%check
make check

# ---------------

%install
%make_install

# Fedora does not support multiple versions of same package installed,
# and the */dir info file (containing all top nodes) is automatically updated
# in the %%post and %%postun phases...
rm -f %{buildroot}%{_bindir}/gawk-%{version}*
rm -f %{buildroot}%{_infodir}/dir

# Create additional symlinks:
ln -sf gawk %{buildroot}%{_bindir}/awk
ln -sf gawk.1.gz %{buildroot}%{_mandir}/man1/awk.1.gz

ln -sf /usr/share/awk   %{buildroot}%{_datadir}/gawk
ln -sf /usr/libexec/awk %{buildroot}%{_libexecdir}/gawk

# Install NLS language files:
%find_lang %{name}

# Install the all the documentation in the same folder - /usr/share/doc/gawk:
install -m 0755 -d %{buildroot}%{_docdir}/%{name}/html/gawk/
install -m 0755 -d %{buildroot}%{_docdir}/%{name}/html/gawkinet/

install -m 0644 -p html/gawk/*           %{buildroot}%{_docdir}/%{name}/html/gawk/
install -m 0644 -p html/gawkinet/*       %{buildroot}%{_docdir}/%{name}/html/gawkinet/

install -m 0644 -p doc/gawk.{pdf,ps}     %{buildroot}%{_docdir}/%{name}
install -m 0644 -p doc/gawkinet.{pdf,ps} %{buildroot}%{_docdir}/%{name}

# ---------------

# Always update the info pages:
%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

# ---------------

%preun
if [[ $1 -eq 0 ]]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

# === PACKAGING INSTRUCTIONS ==================================================

%files -f %{name}.lang
%{_bindir}/*awk
%{_libdir}/gawk
%{_libexecdir}/*awk
%{_datadir}/*awk

%{_mandir}/man1/*
%{_mandir}/man3/*
%{_infodir}/*awk*.info*

%doc NEWS README POSIX.STD README_d/README.multibyte
%license COPYING LICENSE.GPLv2 LICENSE.LGPLv2 LICENSE.BSD

# ---------------

%files devel
%{_includedir}/gawkapi.h

# ---------------

# NOTE: For some reason, adding all files in one line causes RPM build to fail.
%files doc
%doc %{_docdir}/%{name}/gawk.{pdf,ps}
%doc %{_docdir}/%{name}/gawkinet.{pdf,ps}
%doc %{_docdir}/%{name}/html

# =============================================================================

%changelog
* Fri Sep 15 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 4.1.4-7
- Revert previous change of adding 'awk*' symlinks for info pages (bug #1486924)
- Added patch to correctly fix the info pages issue (bug #1486924)
- specfile content refactored for better readability

* Thu Aug 31 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 4.1.4-6
- Added 'awk*' symlinks for info pages (bug #1486924)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.1.4-2
- Rebuild for readline 7.x

* Mon Sep 12 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 4.1.4-1
- Update to latest stable release from upstream

* Mon Sep 12 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 4.1.3-9
- Build gawk with readline support (useful for gawk debugger)

* Mon Sep 12 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 4.1.3-8
- Support for GNU MPFR added (see 'man gawk', look for --bignum option)
- Another round of specfile refactoring

* Sun Sep 11 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 4.1.3-7
- Trailing '%' character removed from doc subpackage's NVR

* Sun Sep 11 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 4.1.3-6
- New gawk-doc subpackage created (contains HTML, PDF and PS documentation)

* Thu Sep  8 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 4.1.3-5
- New gawk-devel subpackage created (contains gawkapi.h header file)

* Tue Sep  6 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 4.1.3-4
- License field updated to more correctly reflect the actual licenses used,
  other licensing issues fixed as well
- Major specfile refactoring to comply with latest Fedora Packaging Guidelines

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 jchaloup <jchaloup@redhat.com> - 4.1.3-1
- Update to upstream 4.1.3
  resolves: #1223594

* Wed Apr 29 2015 jchaloup <jchaloup@redhat.com> - 4.1.2-1
- Update to upstream 4.1.2
  resolves: #1217027

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 4.1.1-7
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Jan 02 2015 jchaloup <jchaloup@redhat.com> - 4.1.1-6
- No need for build dependency on byacc/bison, fix make check
  resolves: #1176993
  resolves: #1177001

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 4.1.1-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 jchaloup <jchaloup@redhat.com> - 4.1.1-2
- resolves: #1089073
  eval invalid free

* Mon Apr 21 2014 Ondrej Vasik <ovasik@redhat.com> - 4.1.1-1
- Update to upstream 4.1.1 (#1087242)

* Sat Jan 25 2014 Ville Skytta <ville.skytta@iki.fi> - 4.1.0-3
- Own the %%{_libdir}/gawk dir.
- Use xz compressed upstream tarball.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Fridolin Pokorny <fpokorny@redhat.com> -  4.1.0-1
- Update to upstream 4.1.0 (#962109)
- Removed FUTURES and LIMITATIONS
- Added unpackaged files

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Martin Briza <mbriza@redhat.com> - 4.0.2-1
- Update to upstream 4.0.2 (#890559)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Martin Briza <mbriza@redhat.com> -  4.0.1-1
- Update to upstream 4.0.1 (#808005)
- Corrected Source0 link to .tar.gz extension as not all releases are available as .tar.bz2
- Resolves #724817 - gawk-4.0.0 regression in '\' escape handling in gsub()
- Resolves #820550 - gawk: getline in BEGIN skips 2 lines

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 4.0.0-4
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 4.0.0-3
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 14 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 4.0.0-1
- Remove gawk-3.1.8-syntax.patch, gawk-3.1.8-double-free-wstptr.patch
- Update to upstream 4.0.0 (#717885)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 02 2010 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 3.1.8-3
- fix syntax issues #528623, #528625
- add byacc to BuildRequires
- follow updated libsigsegv option in configure script

* Tue Nov 02 2010 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 3.1.8-2
- fix #629196: Double free in free_wstr
- fix license tag, add description
- remove BuildRoot tag

* Fri May  7 2010 Stepan Kasal <kasal@ucw.cz> - 3.1.8-1
- new upstream version
- drop upstreamed patches

* Thu Apr 01 2010 Jan Zeleny <jzeleny@redhat.com> - 3.1.7-3
- fix issue with utf8 precision recognition (#513234)

* Thu Oct  8 2009 Stepan Kasal <skasal@redhat.com> - 3.1.7-2
- in posix mode, make ARGV[0] = argv[0] (#525381)

* Wed Sep  9 2009 Stepan Kasal <skasal@redhat.com> - 3.1.7-1
- new upstream version
- disable libsigsegv

* Fri Jul 24 2009 Fed Rel Eng <rel-eng@lists.fedoraproject.org> - 3.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fed Rel Eng <rel-eng@lists.fedoraproject.org> - 3.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Stepan Kasal <skasal@redhat.com> - 3.1.6-4
- remove the versioned binaries even if the version is modified by the
  snapshot patch, modify the file list to check this (#476166)
- update the snapshot patch, dropping the upstreamed
  gawk-3.1.5-test-lc_num1.patch

* Thu Dec 11 2008 Stepan Kasal <skasal@redhat.com> - 3.1.6-3
- grab the current stable tree from savannah

* Wed Nov 26 2008 Stepan Kasal <skasal@redhat.com> - 3.1.6-2
- test-lc_num1.patch submitted upstream, link added

* Tue Nov 25 2008 Stepan Kasal <skasal@redhat.com> - 3.1.6-1
- new upstream version
- drop Patch1: gawk-3.1.3-getpgrp_void.patch, it seems to be a workaround
  for a bug in gcc that seemed to exist at Fedora Core 1 times, see #114246
- drop patches 2-13, they have been integrated upstream

* Mon Jul 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1.5-18
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.1.5-17
- Autorebuild for GCC 4.3

* Wed Oct 31 2007 Stepan Kasal <skasal@redhat.com> - 3.1.5-16
- Add gawk-3.1.5-quote-sticky.patch
- Resolves: #299551
- Add gawk-3.1.5-test-lc_num1.patch, a test for that bug.
- BuldRequire autoconf and automake, for the test patch.
- Add coment explaining why bison is buildrequired.
- Remove BuildRequire: flex.

* Mon Feb 12 2007 Karel Zak <kzak@redhat.com> 3.1.5-15
- fix #225777 - clean up spec file according to Fedora Merge Review
  suggestions (thanks to Dan Horak and Patrice Dumas)

* Mon Jan 15 2007 Karel Zak <kzak@redhat.com> 3.1.5-14
- sync with double-free upstream fixes
- fix #222531: Replace dist by ?dist

* Fri Jan 12 2007 Karel Zak <kzak@redhat.com> 3.1.5-13
- fix MB read 

* Fri Jan 12 2007 Karel Zak <kzak@redhat.com> 3.1.5-13
- improve freewstr patch

* Thu Jan 11 2007 Karel Zak <kzak@redhat.com> 3.1.5-12
- fix #222080 double free or corruption

* Wed Jul 19 2006 Karel Zak <kzak@redhat.com> 3.1.5-11
- spec file cleanup

* Tue Jul 18 2006 Karel Zak <kzak@redhat.com> 3.1.5-10
- add IPv6 support (patch be Jan Pazdziora)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.1.5-9.1
- rebuild

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
