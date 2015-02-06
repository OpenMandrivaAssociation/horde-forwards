%define	module	forwards

Name:		horde-%{module}
Version:	3.2.1
Release:	5
Summary:	The Horde forwards management application
License:	GPL
Group:		System/Servers
URL:		http://www.horde.org/%{module}/
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Requires:	horde >= 3.3.8
BuildArch:	noarch

%description
Forwards is a Horde module for setting user e-mail forwards with support for
several popular mailers. While it has been released and is in production use at
many sites, it is also still under development in an effort to expand and
improve the module.

Right now, Forwards provides fairly complete support for setting .forward style
forwards on sendmail or courier mail based systems via an FTP transport. It now
also supports for mdaemon, and qmail and exim sql based systems.

Forwards is part of a suite of account management modules for Horde consisting
of Accounts, Forwards, Passwd, and Vacation.

%prep
%setup -q -n %{module}-h3-%{version}

# fix perms
find lib -type f | xargs chmod 644

%build

%install
rm -rf %{buildroot}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Require all denied
</Directory>
EOF

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
cat > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php <<'EOF'
<?php
//
// Forwards Horde configuration file
//
 
$this->applications['forwards'] = array(
    'fileroot'    => $this->applications['horde']['fileroot'] . '/forwards',
    'webroot'     => $this->applications['horde']['webroot'] . '/forwards',
    'name'        => _("Forwards"),
    'status'      => 'active',
    'provides'    => 'forwards',
    'menu_parent' => 'myaccount',
);
EOF

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
cp -pR *.php %{buildroot}%{_datadir}/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR themes %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

install -d -m 755 %{buildroot}%{_sysconfdir}/horde
pushd %{buildroot}%{_datadir}/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
popd

%clean
rm -rf %{buildroot}



%files
%defattr(-,root,root)
%doc LICENSE README docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}



%changelog
* Sun Aug 08 2010 Thomas Spuhler <tspuhler@mandriva.org> 3.2.1-1mdv2011.0
+ Revision: 567487
- Updated to version 3.2.1
- added version 3.2.1

* Tue Aug 03 2010 Thomas Spuhler <tspuhler@mandriva.org> 3.1-6mdv2011.0
+ Revision: 565210
- Increased release for rebuild

* Mon Jan 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 3.1-5mdv2010.1
+ Revision: 493343
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise
- restrict default access permissions to localhost only, as per new policy

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.1-3mdv2010.0
+ Revision: 446056
- new setup (simpler is better)

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 3.1-2mdv2010.0
+ Revision: 437881
- rebuild

* Thu Mar 19 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.1-1mdv2009.1
+ Revision: 358196
- update to new version 3.1

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 3.0-5mdv2009.0
+ Revision: 246877
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-3mdv2008.1
+ Revision: 132441
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Fri Aug 25 2006 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-2mdv2007.0
- Rebuild

* Mon Mar 13 2006 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-1mdk
- new version
- %%mkrel

* Thu Jun 30 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.2-1mdk 
- new version
- better fix encoding
- spec cleanup

* Fri Feb 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.2.1-3mdk
- spec file cleanups, remove the ADVX-build stuff
- strip away annoying ^M

* Fri Jan 14 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.2.1-2mdk 
- top-level is now /var/www/horde/forwards
- config is now in /etc/horde/forwards
- other non-accessible files are now in /usr/share/horde/forwards
- no more apache configuration
- rpmbuildupdate aware
- spec cleanup

* Sat Sep 04 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.2.1-1mdk 
- first mdk release

