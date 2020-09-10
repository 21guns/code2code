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
	<artifactId>admin-controller</artifactId>
	<version>${v}</version>
	<packaging>jar</packaging>
	<name>${module_name}-admin-controller</name>

	<properties>
	</properties>

	<dependencies>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
			<exclusions>
				<exclusion>
					<groupId>org.springframework.boot</groupId>
					<artifactId>spring-boot-starter-tomcat</artifactId>
				</exclusion>
			</exclusions>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-undertow</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-actuator</artifactId>
		</dependency>
		<dependency>
		<groupId>com.${package_name.replace('/', '.')}.${module_name}</groupId>
			<artifactId>service</artifactId>
			<version>${v}</version>
		</dependency>
		<dependency>
			<groupId>mysql</groupId>
			<artifactId>mysql-connector-java</artifactId>
			<scope>runtime</scope>
		</dependency>
		<dependency>
			<groupId>com.guns21</groupId>
			<artifactId>spring-data</artifactId>
		</dependency>
	</dependencies>


</project>
