<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
	<%v = '${release.version}'%>
	<modelVersion>4.0.0</modelVersion>
	<parent>
		<groupId>${package_name}</groupId>
		<artifactId>parent</artifactId>
		<version>0.0.1-SNAPSHOT</version>
		<relativePath/> <!-- lookup parent from repository -->
	</parent>

	<groupId>${package_name}.${module_name}</groupId>
	<artifactId>api</artifactId>
	<version>${v}</version>
	<packaging>jar</packaging>
	<name>${module_name}-api</name>

	<dependencies>
		<dependency>
			<groupId>org.projectlombok</groupId>
			<artifactId>lombok</artifactId>
		</dependency>
		<dependency>
			<groupId>com.guns21</groupId>
			<artifactId>common</artifactId>
		</dependency>	
	</dependencies>

</project>
