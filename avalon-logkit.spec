Name:		avalon-logkit
Version:	2.2.1
Release:	2
Summary:	Java logging toolkit
Group:		Development/Java
License:	Apache-2.0
URL:		https://avalon.apache.org/logkit/
# Java sources from the 2.2.1 sources jar, repacked so the lookaside
# archive is not a jar. FreeMarker looks up both jar filenames.
Source0:	avalon-logkit-%{version}.tar.gz
Patch0:		logkit-2.2.1-compile.patch

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	sysjar
BuildRequires:	javapackages-filesystem
BuildRequires:	jmod(java.jms)
BuildRequires:	jmod(javax.servlet)
BuildRequires:	jmod(java.mail)
BuildRequires:	jmod(org.apache.log4j.v12)

%description
LogKit %{version} is the logging toolkit FreeMarker compiles against.
The same classes are installed as avalon-logkit.jar and org.apache.log.jar.
DefaultDataSource implements the JDBC 4 methods of javax.sql.DataSource.

%prep
%autosetup -n avalon-logkit-%{version} -p1
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
find . -type d -name '*.jar' -print >> binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi

%build
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH="$JAVA_HOME/bin:$PATH"
find . -name '*.java' > sources.list
test "$(wc -l < sources.list)" -eq 61
mkdir -p classes
CP=%{_javadir}/javax.servlet.jar:%{_javadir}/java.mail.jar:%{_javadir}/javax.jms-api.jar:%{_javadir}/log4j.jar
javac --release 8 -encoding UTF-8 -Xlint:-options,-removal -proc:none \
	-cp "$CP" -d classes @sources.list
echo 'Automatic-Module-Name: org.apache.log' > avalon-logkit.mf
jar cfm avalon-logkit.jar avalon-logkit.mf -C classes .
jar i avalon-logkit.jar
javap -v -classpath avalon-logkit.jar org.apache.log.Logger | grep -F -q 'major version: 52'
desc=$(jar --describe-module --file avalon-logkit.jar)
printf '%s\n' "$desc" | grep -F -q 'org.apache.log'
if printf '%s\n' "$desc" | grep -F -q 'Unable'; then
	exit 1
fi

cat > avalon-logkit.pom << END
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.apache.avalon.logkit</groupId>
  <artifactId>avalon-logkit</artifactId>
  <version>%{version}</version>
  <name>Avalon LogKit</name>
  <description>Logging toolkit used by FreeMarker.</description>
  <url>https://avalon.apache.org/logkit/</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
      <distribution>repo</distribution>
    </license>
  </licenses>
</project>
END

%install
sysjar install --buildroot %{buildroot} \
	--artifact avalon-logkit.pom:avalon-logkit.jar \
	--file-name avalon-logkit \
	--link org.apache.log \
	--filelist .mfiles

%check
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH="$JAVA_HOME/bin:$PATH"
test -s %{buildroot}%{_javadir}/avalon-logkit.jar
test -L %{buildroot}%{_javadir}/org.apache.log.jar
mkdir -p check
cat > check/Smoke.java << 'EOF'
import java.io.StringWriter;

import org.apache.log.Hierarchy;
import org.apache.log.LogTarget;
import org.apache.log.Logger;
import org.apache.log.Priority;
import org.apache.log.format.RawFormatter;
import org.apache.log.output.io.WriterTarget;

public class Smoke {
	public static void main(String[] args) {
		StringWriter writer = new StringWriter();
		WriterTarget target = new WriterTarget(writer, new RawFormatter());
		Hierarchy hierarchy = new Hierarchy();
		Logger log = hierarchy.getLoggerFor(args[1]);
		log.setAdditivity(false);
		log.setPriority(Priority.INFO);
		log.setLogTargets(new LogTarget[] { target });
		log.info(args[0]);
		String text = writer.toString();
		if (!text.equals(args[0])) {
			throw new AssertionError(text);
		}
		System.out.println(args[0] + " " + args[1] + " " + text);
	}
}
EOF
JAR=%{buildroot}%{_javadir}/avalon-logkit.jar
javac --release 8 -encoding UTF-8 -proc:none -cp "$JAR" -d check check/Smoke.java
java -cp "check:$JAR" Smoke avalon_ok gradle > check/out.txt
cat check/out.txt
grep -F -q 'avalon_ok gradle avalon_ok' check/out.txt

%files -f .mfiles
%license LICENSE
