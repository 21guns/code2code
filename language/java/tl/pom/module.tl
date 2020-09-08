<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
	<%v = '${com.version}'%>
	<modelVersion>4.0.0</modelVersion>

	<groupId>com.${package_name.replace('/', '.')}</groupId>
	<artifactId>${module_name}</artifactId>
	<version>${v}</version>
	<packaging>pom</packaging>

	<name>${module_name}</name>
	<description>${module_name}</description>

	<parent>
		<groupId>com.ktjr.lcl</groupId>
		<artifactId>parent</artifactId>
		<version>0.0.1-SNAPSHOT</version>
		<relativePath/> <!-- lookup parent from repository -->
	</parent>

	<modules>
		<module>admin-controller</module>
		<module>api</module>
		<module>controller</module>
		<module>service</module>
	</modules>

</project>
