# 根据excel md 生成java代码

# 项目介绍
参考DDD，CQRS架构，生成基于Spring boot Mybatis的微服务架构的代码

## core代码继承关系
metadata
    Module
    Table
        Field
    Action
        UrlPath
        Request
        Response
            Paramter

Language 
    Java
        Class
        Enum
        
    XML
    Sql

Module



java
    JavaClass
    DTO
    DO
    VO
    Controller
    Service
    Respository
    Mapper

## java代码架构 
Query(extends DTO) ----------------->  

Controller --> QueryService --> Mapper

<--------------------------------- DTO

DTO --------- DTO ---------> DO ---------------------->

Controller --> CommandService --> Repository --> Mapper

<------------ DTO <--------- DO --------------------- DO 



Repository = 数据仓库 ：包含事务处理