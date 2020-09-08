<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
	<%v = '${com.version}'%>
	<modelVersion>4.0.0</modelVersion>
	<parent>
		<groupId>com.${package_name.replace('/', '.')}</groupId>
		<artifactId>parent</artifactId>
		<version>0.0.1-SNAPSHOT</version>
		<relativePath/> <!-- lookup parent from repository -->
	</parent>

	<groupId>com.${package_name.replace('/', '.')}.${module_name}</groupId>
	<artifactId>api</artifactId>
	<version>${v}</version>
	<packaging>jar</packaging>
	<name>${module_name}-api</name>

	<dependencies>
		<dependency>
			<groupId>org.projectlombok</groupId>
			<artifactId>lombok</artifactId>
		</dependency>
	</dependencies>

</project>
