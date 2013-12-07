%define gcj_support     1
%define short_name      logkit
%define section         free

Name:           avalon-%{short_name}
Version:        2.1
Release:        8
Epoch:          0
Summary:        Java logging toolkit
License:        Apache License
Group:          Development/Java
Url:            http://avalon.apache.org/%{short_name}/
Source0:        http://www.apache.org/dist/excalibur/avalon-logkit/source/avalon-logkit-2.1-src.tar.bz2
Patch0:         %{name}-build.patch
Patch1:			fix-java6-compile.patch
Requires:       avalon-framework >= 0:4.1.4
Requires:       geronimo-servlet-2.4-api
Requires:       geronimo-jms-1.1-api
Requires:       jdbc-stdext
BuildRequires:  locales-en
BuildRequires:  java-1.6.0-openjdk-devel
BuildRequires:  java-rpmbuild
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  ant ant-nodeps
BuildRequires:  avalon-framework-javadoc
BuildRequires:  classpathx-mail
BuildRequires:  java-javadoc
BuildRequires:  log4j
BuildRequires:  avalon-framework >= 0:4.1.4
BuildRequires:  geronimo-servlet-2.4-api
BuildRequires:  geronimo-jms-1.1-api
BuildRequires:  jdbc-stdext
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif

%description
LogKit is a logging toolkit designed for secure performance orientated
logging in applications. To get started using LogKit, it is recomended
that you read the whitepaper and browse the API docs.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%patch0 -p1 -b .build
%patch1 -p0 -b .java6
%{_bindir}/find . -name "*.jar" | %{_bindir}/xargs -t %{__rm} -f
%{__perl} -pi -e 's/1\.2/1\.4/g' build.xml

%build
export LC_ALL=ISO-8859-1
export CLASSPATH=$(build-classpath log4j javamail/mailapi jms servlet jdbc-stdext avalon-framework)
%{ant} -Dbuild.sysclasspath=only --execdebug\
       -Djava.javadoc=%{_javadocdir}/java \
       -Davalon.javadoc=%{_javadocdir}/avalon-framework \
  clean jar javadoc

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt NOTICE.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}




%changelog
* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 2.1-3mdv2008.0
+ Revision: 87213
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Sep 08 2007 Pascal Terjan <pterjan@mandriva.org> 0:2.1-2mdv2008.0
+ Revision: 82623
- update to new version


* Wed Dec 13 2006 David Walluck <walluck@mandriva.org> 2.1-1mdv2007.0
+ Revision: 96163
- 2.1

* Mon Dec 11 2006 David Walluck <walluck@mandriva.org> 0:1.2-3.2mdv2007.1
+ Revision: 95106
- Import avalon-logkit

* Sat Jun 03 2006 David Walluck <walluck@mandriva.org> 0:1.2-3.2mdv2007.0
- fix build
- own %%{_libdir}/gcj/%%{name}
- rebuild for libgcj.so.7

* Fri Dec 02 2005 David Walluck <walluck@mandriva.org> 0:1.2-3.1mdk
- sync with 3jpp
- aot-compile

* Fri May 13 2005 David Walluck <walluck@mandriva.org> 0:1.2-2.1mdk
- release

* Tue Jan 11 2005 Gary Benson <gbenson@redhat.com> 0:1.2-2jpp_4fc
- Reenable building of classes that require javax.swing (#130006).

* Thu Nov 04 2004 Gary Benson <gbenson@redhat.com> 0:1.2-2jpp_3fc
- Build into Fedora.

* Fri Oct 29 2004 Gary Benson <gbenson@redhat.com> 0:1.2-2jpp_2fc
- Bootstrap into Fedora.

* Fri Mar 05 2004 Frank Ch. Eigler <fche@redhat.com> 0:1.2-2jpp_1rh
- RH vacuuming

