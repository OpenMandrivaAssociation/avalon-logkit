%define gcj_support     1
%define short_name      logkit
%define section         free

Name:           avalon-%{short_name}
Version:        2.1
Release:        %mkrel 1
Epoch:          0
Summary:        Java logging toolkit
License:        Apache License
Group:          Development/Java
Url:            http://avalon.apache.org/%{short_name}/
Source0:        http://www.apache.org/dist/excalibur/avalon-logkit/source/avalon-logkit-2.1-src.tar.bz2
Patch0:         %{name}-build.patch
Requires:       avalon-framework >= 0:4.1.4
Requires:       servlet
Requires:       jms
Requires:       jdbc-stdext
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  ant
BuildRequires:  avalon-framework-javadoc
BuildRequires:  javamail
BuildRequires:  java-javadoc
BuildRequires:  log4j
BuildRequires:  avalon-framework >= 0:4.1.4
BuildRequires:  servlet
BuildRequires:  jms
BuildRequires:  jdbc-stdext
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
%else
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
%{_bindir}/find . -name "*.jar" | %{_bindir}/xargs -t %{__rm} -f
%{__perl} -pi -e 's/1\.2/1\.4/g' build.xml

%build
export CLASSPATH=$(build-classpath log4j javamail/mailapi jms servlet jdbc-stdext avalon-framework)
%{ant} -Dbuild.sysclasspath=only \
       -Djava.javadoc=%{_javadocdir}/java \
       -Davalon.javadoc=%{_javadocdir}/avalon-framework \
  clean jar javadoc

%install
%{__rm} -rf %{buildroot}

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

%clean
%{__rm} -rf %{buildroot}

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


