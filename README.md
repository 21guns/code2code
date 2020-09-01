# 根据excel生产java代码

# 项目介绍
参考DDD，CQRS架构，
生产基于Spring boot Mybatis的微服务架构的代码

## 相关架构 
Query(extends DTO) ----------------->  

Controller --> QueryService --> Mapper

<--------------------------------- DTO

DTO --------- DTO ---------> DO ---------------------->

Controller --> CommandService --> Repository --> Mapper

<------------ DTO <--------- DO --------------------- DO 



Repository = 数据仓库 ：包含事务处理