%global     short_name      logkit
%global     camelcase_short_name      LogKit

Name:        avalon-%{short_name}
Version:     2.2.1
Release:     1
Summary:     Java logging toolkit
License:     ASL 2.0
Group:       Development/Java
URL:         http://avalon.apache.org/%{short_name}/
Source0:     https://repo1.maven.org/maven2/org/apache/avalon/logkit/avalon-logkit/%{version}/avalon-logkit-%{version}-sources.jar
Source1:     https://repo1.maven.org/maven2/org/apache/avalon/logkit/avalon-logkit/%{version}/avalon-logkit-%{version}.pom
Patch0:		logkit-2.2.1-compile.patch
BuildRequires:	jdk-current
BuildRequires:	javapackages-local
BuildRequires:	jmod(java.jms)
BuildRequires:	jmod(javax.servlet)
BuildRequires:	jmod(java.mail)
BuildRequires:	jmod(org.apache.log4j.v12)

BuildArch:    noarch


%description
LogKit is a logging toolkit designed for secure performance orientated
logging in applications. To get started using LogKit, it is recomended
that you read the whitepaper and browse the API docs.

%package javadoc
Summary:    Javadoc for %{name}
Group:        Documentation
Requires:     jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%autosetup -p1 -c %{name}-%{version}

%build
export LANG=en_US.utf-8
. %{_sysconfdir}/profile.d/90java.sh

buildjar() {
	if ! [ -e module-info.java ]; then
		MODULE="$1"
		shift
		echo "module $MODULE {" >module-info.java
		find . -name "*.java" |xargs grep ^package |sed -e 's,^.*package ,,;s,\;.*,,' -e 's/^[[:space:]]*//g' -e 's/[[:space:]]*\$//g' |sort |uniq |while read e; do
			echo "  exports $e;" >>module-info.java
		done
		for i in "$@"; do
			echo "	requires $i;" >>module-info.java
		done
		echo '}' >>module-info.java
	fi
	find . -name "*.java" |xargs javac -p %{_javadir}/modules
	find . -name "*.class" -o -name "*.properties" |xargs jar cf $MODULE-%{version}.jar
	jar i $MODULE-%{version}.jar
	# Javadoc for javax.servlet is broken and in need of compile
	# fixes
	javadoc -d docs -p %{_javadir}/modules -sourcepath . $MODULE
}

buildjar org.apache.log java.jms javax.servlet java.mail org.apache.log4j.v12 java.sql

%install
mkdir -p %{buildroot}%{_javadir}/modules %{buildroot}%{_mavenpomdir} %{buildroot}%{_javadocdir}
cp org.apache.log-%{version}.jar %{buildroot}%{_javadir}/modules
ln -s modules/org.apache.log-%{version}.jar %{buildroot}%{_javadir}/
ln -s modules/org.apache.log-%{version}.jar %{buildroot}%{_javadir}/org.apache.log.jar
ln -s modules/org.apache.log-%{version}.jar %{buildroot}%{_javadir}/avalon-logkit.jar
ln -s modules/org.apache.log-%{version}.jar %{buildroot}%{_javadir}/avalon-logkit-%{version}.jar
cp %{S:1} %{buildroot}%{_mavenpomdir}/
%add_maven_depmap avalon-logkit-%{version}.pom org.apache.log-%{version}.jar
mv docs %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%{_javadir}/*.jar
%{_javadir}/modules/*.jar

%files javadoc
%{_javadocdir}/%{name}
