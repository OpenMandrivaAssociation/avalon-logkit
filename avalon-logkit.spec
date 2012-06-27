# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global     short_name      logkit
%global     camelcase_short_name      LogKit

Name:        avalon-%{short_name}
Version:     2.1
Release:     7
Summary:     Java logging toolkit
License:     ASL 1.1
Group:       Development/Java
URL:         http://avalon.apache.org/%{short_name}/
Source0:     http://www.apache.org/dist/excalibur/%{name}/source/%{name}-%{version}-src.zip
Source1:     http://repo1.maven.org/maven2/avalon-logkit/avalon-logkit/%{version}/%{name}-%{version}.pom
Patch0:      fix-java6-compile.patch
Patch1:      avalon-logkit-pom-deps.patch
Patch2:      avalon-logkit-encoding.patch
Patch3:      java7.patch
Requires:    avalon-framework >= 0:4.1.4
Requires:    tomcat-servlet-3.0-api
Requires:    jms

BuildRequires:    jpackage-utils >= 0:1.5
BuildRequires:    ant
BuildRequires:    javamail
BuildRequires:    ant-junit
BuildRequires:    log4j
BuildRequires:    avalon-framework >= 0:4.1.4
# Required for converting jars to OSGi bundles
BuildRequires:    aqute-bndlib
BuildRequires:    tomcat-servlet-3.0-api
BuildRequires:    jms

BuildArch:    noarch


%description
LogKit is a logging toolkit designed for secure performance orientated
logging in applications. To get started using LogKit, it is recomended
that you read the whitepaper and browse the API docs.

%package javadoc
Summary:    Javadoc for %{name}
Group:        Development/Java
Requires:     jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%patch0

cp %{SOURCE1} pom.xml
%patch1
%patch2 -p1
%patch3
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%build
export CLASSPATH=%(build-classpath log4j javamail/mailapi jms servlet jdbc-stdext avalon-framework junit):$PWD/build/classes
ant -Dencoding=ISO-8859-1 -Dnoget=true clean jar javadoc
# Convert to OSGi bundle
java -jar $(build-classpath aqute-bndlib) wrap target/%{name}-%{version}.jar

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}/%{_mavenpomdir}

install -m 644 target/%{name}-%{version}.bar %{buildroot}%{_javadir}/%{name}.jar

install -pm 644 pom.xml %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar -a "%{short_name}:%{short_name},org.apache.avalon.logkit:%{name}"

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}

%files
%doc LICENSE.txt NOTICE.txt
%{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/JPP-%{name}.pom
%{_javadir}/%{name}.jar

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/%{name}

