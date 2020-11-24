# 根据excel md 生成java代码

# 项目介绍
参考DDD，CQRS架构，生成基于Spring boot Mybatis的微服务架构的代码

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