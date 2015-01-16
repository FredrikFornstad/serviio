Name: 		serviio
Version:	1.5
Release:	3
License:	Free to use, copy & redistribute with limitations. See LICENCE.txt in Source file.
Summary:	A free media server
URL:		http://www.serviio.org/
Group:		Productivity/Multimedia/Other
Source:		http://download.serviio.org/releases/%{name}-%{version}-linux.tar.gz
Source1:	serviio
Patch1:     	serviio.sh.patch
Patch2:		profiles.xml.patch
BuildRequires:	tar gzip
Requires:   	java-1.8.0-openjdk
Requires:	ffmpeg >= 0.11
Requires:	dcraw >= 8.96
BuildRoot:  	%{_tmppath}/%{name}-%{version}-build
BuildArch:	noarch

%description
It allows you to stream your media files (music, video 
or images) to renderer devices (e.g. a TV set, Bluray player, games console
or mobile phone) on your connected home network.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%__cp %{SOURCE1} .

%build

%install
chmod 775 bin/*.sh
install -d $RPM_BUILD_ROOT/usr/share/serviio/bin
%__cp bin/*.sh $RPM_BUILD_ROOT/usr/share/serviio/bin 
chmod -x library/derby.properties
for dir in config lib library plugins; do 
	install -d $RPM_BUILD_ROOT/usr/share/serviio/$dir
	%__cp $dir/* $RPM_BUILD_ROOT/usr/share/serviio/$dir
done
install -d $RPM_BUILD_ROOT/usr/share/serviio/log
install -D -m 755 %{S:1} $RPM_BUILD_ROOT/etc/init.d/serviio


%pre
getent group serviio >/dev/null || groupadd -r serviio
getent passwd serviio >/dev/null || useradd -r -g serviio -d /usr/share/serviio -s /sbin/nologin -c "Serviio Deamon" serviio


%post
chkconfig --add serviio
# chkconfig serviio on
# service serviio start

%preun
if [ $1 -eq 0 ] ; then  # If this is an unistall then stop and delete the Serviio service
	service serviio stop >/dev/null 2>&1
	chkconfig serviio off
	chkconfig --del serviio
fi

%postun
if [ "$1" -ge "1" ] ; then  # If this is an upgrade then restart Serviio
	service serviio condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,%{name},%{name})
%doc legal/commons-codec-licence.txt legal/commons-io-licence.txt legal/dcraw-licence.txt legal/Derby-licence.txt legal/FFmpeg-licence.txt legal/FreeMarker-licence.txt legal/Gson-licence.txt legal/HttpCore-licence.txt legal/Jcs-licence.txt legal/JDOM-licence.txt legal/jNAT-PMPlib-licence.txt legal/LameMP3Encoder-licence.txt legal/librtmp-licence.txt legal/LICENSE.xerox legal/Log4J-licence.txt legal/Restlet-licence.txt legal/Rome-licence.txt legal/Sanselan-licence.txt legal/sbbi-upnplib-licence.txt legal/slf4j-licence.txt legal/StreamFlyer-licence.txt legal/winp-licence.txt legal/XStream-licence.txt LICENCE.txt NOTICE.txt README.txt RELEASE_NOTES.txt
%attr(-,%{name},%{name}) /usr/share/serviio
%attr(755,root,root) /etc/init.d/serviio

%changelog
* Fri Jan 16 2015 Fredrik Fornstad <fredrik.fornstad@gmail.com> - 1.5-3
- New upstream release
- Java 8 is now required, DTS-patch introduced as Serviio 1.5 is designed for FFmpeg 2.3 or higher

* Sat Mar 22 2014 Fredrik Fornstad <fredrik.fornstad@gmail.com> - 1.4.1.2
- New upstream release

* Wed Mar 19 2014 Fredrik Fornstad <fredrik.fornstad@gmail.com> - 1.4.1.1
- New upstream release

* Sat Mar 15 2014 Fredrik Fornstad <fredrik.fornstad@gmail.com> - 1.4.1
- New release of upstream Serviio
- Change so that Serviio running state is preserved at future upgrades

* Fri Jan 10 2014 Fredrik Fornstad <fredrik.fornstad@gmail.com> - 1.4
- New version of Serviio

* Sun Nov 10 2013 Fredrik Fornstad <fredrik.fornstad@gmail.com> - 1.3.1
- First build for ClearOS 6

