Name:      elinks
Summary:   A text-mode Web browser
Version:   0.12
Release:   0.5.pre2%{?dist}
License:   GPLv2
URL:       http://elinks.or.cz
Group:     Applications/Internet
Source:    http://elinks.or.cz/download/elinks-%{version}pre2.tar.bz2
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: automake
BuildRequires: openssl-devel
BuildRequires: bzip2-devel
BuildRequires: expat-devel
BuildRequires: libidn-devel
Requires: zlib >= 1.2.0.2

Provides:  webclient
Obsoletes: links
Provides:  links
Provides: text-www-browser

Patch0: elinks-0.11.0-ssl-noegd.patch
Patch1: elinks-0.10.1-utf_8_io-default.patch
Patch2: elinks-0.10.1-pkgconfig.patch
Patch3: elinks-0.11.0-getaddrinfo.patch
Patch4: elinks-0.11.0-sysname.patch
Patch5: elinks-0.10.1-xterm.patch
Patch6: elinks-0.11.0-union.patch
Patch7: elinks-0.11.3-macropen.patch
Patch8: elinks-scroll.patch

%description
Links is a text-based Web browser. Links does not display any images,
but it does support frames, tables and most other HTML tags. Links'
advantage over graphical browsers is its speed--Links starts and exits
quickly and swiftly displays Web pages.

%prep
%setup -q -n %{name}-%{version}pre2

# Prevent crash when HOME is unset (bug #90663).
%patch0 -p1
# UTF-8 by default
%patch1 -p1
%patch2 -p1
# Make getaddrinfo call use AI_ADDRCONFIG.
%patch3 -p1
# Don't put so much information in the user-agent header string (bug #97273).
%patch4 -p1
# Fix xterm terminal: "Linux" driver seems better than "VT100" (#128105)
%patch5 -p1
# Fix #157300 - Strange behavior on ppc64
%patch6 -p1
# fix for open macro in new glibc 
%patch7 -p1
#upstream fix for out of screen dialogs
%patch8 -p1

%build
./autogen.sh

export CFLAGS="$RPM_OPT_FLAGS $(getconf LFS_CFLAGS) -D_GNU_SOURCE"
%configure %{?rescue:--without-gpm} --without-x --with-gssapi \
  --enable-bittorrent
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
ln -s elinks $RPM_BUILD_ROOT%{_bindir}/links
ln -s elinks.1 $RPM_BUILD_ROOT%{_mandir}/man1/links.1
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/locale.alias
%find_lang elinks

%clean
rm -rf $RPM_BUILD_ROOT

%files -f elinks.lang
%defattr(-,root,root)
%doc README SITES TODO COPYING
%{_bindir}/links
%{_bindir}/elinks
%{_mandir}/man1/links.1*
%{_mandir}/man1/elinks.1*
%{_mandir}/man5/*

%changelog
* Mon Sep 29 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.5.pre2
- new upstream bugfix prerelease
- Removed already applied patches for tabreload and bittorrent

* Mon Sep  1 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.4.pre1
- upstream fix for bittorrent protocol
- upstream fix for out of screen bittorrent dialog texts

* Tue Jul 15 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.3.pre1
- get rid off fuzz in patches

* Tue Jul 15 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.2.pre1
- fix a crash when opening tab during page reload

* Tue Jul  1 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.1.pre1
- unstable elinks-0.12 pre1, solves several long-term issues 
  unsolvable (or very hard to solve) in 0.11.4 (like #173411),
  in general is elinks-0.12pre1 considered better than 0.11.4
- dropped patches negotiate-auth, chunkedgzip - included in 0.12pre1,
  modified few others due source code changes

* Sat Jun 21 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-1
- new stable upstream release

* Thu Mar  6 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-0.4.rc1
- new upstream release candidate marked stable

* Thu Feb 21 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-0.3.rc0
- fixed broken output for gzipped chunked pages(#410801)

* Thu Feb 07 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-0.2.rc0
- used -D_GNU_SOURCE instead of ugly hack/patch to 
  have NI_MAXPATH defined

* Wed Feb 06 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-0.1.rc0
- new version marked stable by upstream 0.11.4rc0
- enabled experimental bittorent support(#426702)

* Wed Dec 05 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-7
- rebuilt because of new OpenSSL

* Thu Oct 11 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-6
- generalized text-www-browser requirements(#174566)

* Tue Aug 28 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-5
- rebuilt because of expat 2.0

* Wed Aug 22 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-4
- rebuilt for F8
- changed license tag to GPLv2

* Thu Aug  9 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-3
- fix of open macro(new glibc) by Joe Orton

* Fri Jul 27 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-2
- cleanup of duplicates in buildreq, added license file to doc 
- (package review by Tyler Owen(#225725))

* Tue Jun  5 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-1
- update to new upstream version
- removed patch for #210103 , included in upstream release
- updated patch elinks-0.11.1-negotiate.patch to pass build

* Mon Mar 26 2007 Karel Zak <kzak@redhat.com> 0.11.2-1
- update to new upstream version
- cleanup spec file

* Wed Oct 11 2006 Karel Zak <kzak@redhat.com> 0.11.1-5
- fix #210103 - elinks crashes when given bad HTTP_PROXY

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.11.1-4.1
- rebuild

* Mon Jun 12 2006 Karel Zak <kzak@redhat.com> 0.11.1-4
- improved negotiate-auth patch (faster now)

* Fri Jun  9 2006 Karel Zak <kzak@redhat.com> 0.11.1-3
- added negotiate-auth (GSSAPI) support -- EXPERIMENTAL!

* Mon May 29 2006 Karel Zak <kzak@redhat.com> 0.11.1-2
- update to new upstream version

* Wed May 17 2006 Karsten Hopp <karsten@redhat.de> 0.11.0-3
- add buildrequires bzip2-devel, expat-devel,libidn-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.11.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.11.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 10 2006 Karel Zak <kzak@redhat.com> 0.11.0-2
- use upstream version of srcdir.patch

* Tue Jan 10 2006 Karel Zak <kzak@redhat.com> 0.11.0-1
- update to new upstream version
- fix 0.11.0 build system (srcdir.patch)
- regenerate patches:
     elinks-0.11.0-getaddrinfo.patch, 
     elinks-0.11.0-ssl-noegd.patch,
     elinks-0.11.0-sysname.patch,
     elinks-0.11.0-union.patch

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 0.10.6-2.1
- rebuilt

* Wed Nov  9 2005 Karel Zak <kzak@redhat.com> 0.10.6-2
- rebuild (against new openssl)

* Thu Sep 29 2005 Karel Zak <kzak@redhat.com> 0.10.6-1
- update to new upstream version

* Tue May 17 2005 Karel Zak <kzak@redhat.com> 0.10.3-3
- fix #157300 - Strange behavior on ppc64 (patch by Miloslav Trmac)

* Tue May 10 2005 Miloslav Trmac <mitr@redhat.com> - 0.10.3-2
- Fix checking for numeric command prefix (#152953, patch by Jonas Fonseca)
- Fix invalid C causing assertion errors on ppc and ia64 (#156647)

* Mon Mar 21 2005 Karel Zak <kzak@redhat.com> 0.10.3-1
- sync with upstream; stable 0.10.3

* Sat Mar  5 2005 Karel Zak <kzak@redhat.com> 0.10.2-2
- rebuilt

* Tue Feb  8 2005 Karel Zak <kzak@redhat.com> 0.10.2-1
- sync with upstream; stable 0.10.2

* Fri Jan 28 2005 Karel Zak <kzak@redhat.com> 0.10.1-1
- sync with upstream; stable 0.10.1

* Thu Oct 14 2004 Karel Zak <kzak@redhat.com> 0.9.2-2
- the "Linux" driver seems better than "VT100" for xterm (#128105)

* Wed Oct  6 2004 Karel Zak <kzak@redhat.com> 0.9.2-1
- upload new upstream tarball with stable 0.9.2 release

* Mon Sep 20 2004 Jindrich Novy <jnovy@redhat.com> 0.9.2-0.rc7.4
- 0.9.2rc7.
- changed summary in spec to get rid of #41732, #61499

* Mon Sep 13 2004 Tim Waugh <twaugh@redhat.com> 0.9.2-0.rc4.3
- Avoid symbol clash (bug #131170).

* Fri Aug  6 2004 Tim Waugh <twaugh@redhat.com> 0.9.2-0.rc4.2
- 0.9.2rc4.

* Mon Jul 12 2004 Tim Waugh <twaugh@redhat.com> 0.9.2-0.rc2.2
- Fix elinks -dump -stdin (bug #127624).

* Thu Jul  1 2004 Tim Waugh <twaugh@redhat.com> 0.9.2-0.rc2.1
- 0.9.2rc2.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 0.9.1-3
- Build with LFS support (bug #125064).

* Fri May 28 2004 Tim Waugh <twaugh@redhat.com> 0.9.1-2
- Use UTF-8 by default (bug #76445).

* Thu Mar 11 2004 Tim Waugh <twaugh@redhat.com> 0.9.1-1
- 0.9.1.
- Use %%find_lang.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Dec  8 2003 Tim Waugh <twaugh@redhat.com> 0.4.3-1
- 0.4.3.
- Updated pkgconfig patch.

* Mon Aug 11 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-7.1
- Rebuilt.

* Mon Aug 11 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-7
- Don't require XFree86-libs (bug #102072).

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.4.2-6.2
- rebuild

* Thu Jun 12 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-6.1
- Rebuilt.

* Thu Jun 12 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-6
- Make getaddrinfo call use AI_ADDRCONFIG.
- Don't put so much information in the user-agent header string (bug #97273).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  2 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-4.1
- Rebuild again.

* Mon Jun  2 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-4
- Rebuild.

* Mon May 12 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-3
- Prevent crash when HOME is unset (bug #90663).

* Sun May 04 2003 Florian La Roche <Florian.LaRoche@redhat.de> 0.4.2-2
- use relative symlinks to elinks

* Wed Feb  5 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-1
- 0.4.2 (bug #83273).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 0.3.2-5
- rebuilt

* Thu Jan 16 2003 Tim Waugh <twaugh@redhat.com>
- Fix URL (bug #81987).

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 0.3.2-4
- rebuild

* Mon Dec 23 2002 Tim Waugh <twaugh@redhat.com> 0.3.2-3
- Fix bug #62368.

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- use openssl's pkg-config data, if available

* Wed Nov 20 2002 Tim Powers <timp@redhat.com> 0.3.2-2
- rebuild on all arches

* Tue Aug 20 2002 Jakub Jelinek <jakub@redhat.com> 0.3.2-1
- update to 0.3.2 to fix the DNS Ctrl-C segfaults
- update URLs, the project moved
- include man page

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jan 24 2002 Tim Powers <timp@redhat.com>
- rebuilt against new openssl

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan  2 2002 Preston Brown <pbrown@redhat.com> 0.96-4
- cookie fix

* Thu Sep 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.96-3
- Save some more space in rescue mode

* Wed Jul 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.96-2
- Add the links manual from links.sourceforge.net (RFE #49228)

* Tue Jul  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.96-1
- update to 0.96

* Fri Jun 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- actually run make in build phase

* Tue Jun 12 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Jan  9 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.95

* Mon Jan  1 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94 final

* Sun Dec 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- pre9

* Mon Dec 10 2000 Preston Brown <pbrown@redhat.com>
- Upgraded to pre8.

* Tue Dec  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94pre7
- Minor fixes to the specfile (s/Copyright:/License:/)
- merge rescue stuff

* Fri Nov 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94pre5

* Wed Nov 15 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94pre4

* Tue Oct 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94pre1

* Wed Aug  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.92 (needed - prior versions won't display XHTML properly)

* Thu Jul 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment to work around bugs

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 15 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.84

* Sun Jun 11 2000 Preston Brown <pbrown@redhat.com>
- provides virtual package webclient.

* Thu Jan  6 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- initial RPM
