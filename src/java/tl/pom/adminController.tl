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
			<groupId>org.mybatis.spring.boot</groupId>
			<artifactId>mybatis-spring-boot-starter</artifactId>
		</dependency>
		<dependency>
            <groupId>com.github.pagehelper</groupId>
            <artifactId>pagehelper-spring-boot-starter</artifactId>
        </dependency>
		<dependency>
			<groupId>org.springframework.data</groupId>
			<artifactId>spring-data-commons</artifactId>
		</dependency>
		<dependency>
			<groupId>com.mysql</groupId>
			<artifactId>mysql-connector-j</artifactId>
			<scope>runtime</scope>
		</dependency>
		<dependency>
			<groupId>com.guns21</groupId>
			<artifactId>spring-data</artifactId>
		</dependency>
		<dependency>
			<groupId>${package_name}.${module_name}</groupId>
			<artifactId>service</artifactId>
			<version>${v}</version>
		</dependency>
		<dependency>
			<groupId>${package_name}.${module_name}</groupId>
			<artifactId>api</artifactId>
			<version>${v}</version>
		</dependency>
	</dependencies>


</project>
