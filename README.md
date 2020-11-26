# 根据excel md 生成java代码

# 项目介绍

参考DDD，CQRS架构，生成基于Spring boot Mybatis的微服务架构的代码

## 代码生成规则

- 无接口文档、有数据库设计
api Service Controller 三层代码都根据数据库文档生成
- 有接口文档、有数据库设计
Controller Service Respository 根据接口文档生成
mapper DO 根据数据库设计生成

## src代码继承关系
```
- 标准文档解析后的元数据
metadata 
    Module
    Table
        Field
    Action
        UrlPath
        Request
        Response
            Paramter

- 翻译语言
Language 
    Java
        Class
        Enum
    XML
    Sql

- 业务模块
Module
    Project

- 辅助
Context 上下文配置

java
    JavaClass
    DTO
    DO
    VO
    Controller
    Service
    Respository
    Mapper
```

## java代码架构 
Query(extends DTO) ----------------->  

Controller --> QueryService --> Mapper

<--------------------------------- DTO

DTO --------- DTO ---------> DO ---------------------->

Controller --> CommandService --> Repository --> Mapper

<------------ DTO <--------- DO --------------------- DO 



Repository = 数据仓库 ：包含事务处理

