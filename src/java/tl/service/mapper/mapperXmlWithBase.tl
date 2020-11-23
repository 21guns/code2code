<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >
<mapper namespace="com.${package_name}.${module_name}.service.repository.mapper.${class_name}Mapper" >
	<%
		COLUMNS_LINE_MAX = 80

		colums = []
		colums_line = ""
		colums_start = 0

		colums_as = []
		colums_as_line = ""
		colums_as_start = 0

		values = []
		values_line = ""
		values_start = 0

		for index in  range(len(fields)):

			colums_as_line = ', '.join(map(lambda x : (x.field + " AS " + x.name) if x.field != x.name else x.field, fields[colums_as_start:index]))
			if len(colums_as_line) > COLUMNS_LINE_MAX :
				colums_as.append(colums_as_line)
				colums_as_start = index

			colums_line = ', '.join(map(lambda x : x.field, fields[colums_start:index]))
			if len(colums_line) > COLUMNS_LINE_MAX :
				colums.append(colums_line)
				colums_start = index

			values_line = ', '.join(map(lambda x : "#{" + x.name +", jdbcType=" + x.jdbcType + "}", fields[values_start:index]))
			if len(values_line) > COLUMNS_LINE_MAX :
				values.append(values_line)
				values_start = index

		colums_as_line = ', '.join(map(lambda x : (x.field + " AS " + x.name) if x.field != x.name else x.field, fields[colums_as_start:]))
		if (len(colums_as_line)) > 0:
			colums_as.append(colums_as_line)

		colums_line = ', '.join(map(lambda x : x.field, fields[colums_start:]))
		if (len(colums_line)) > 0:
			colums.append(colums_line)

		values_line = ', '.join(map(lambda x : "#{" + x.name +", jdbcType=" + x.jdbcType + "}", fields[values_start:]))
		if (len(values_line)) > 0:
			values.append(values_line)
	%>
	<resultMap id="${class_name}ResultMap" type="com.${package_name}.${module_name}.service.entity.${class_name}DO" >
		% for index in  range(len(fields)):
			% if fields[index].name == "id" :
		<id column="id" property="id" jdbcType="${fields[index].jdbcType}" />
			% else:
		<result column="${fields[index].field}" property="${fields[index].name}" jdbcType="${fields[index].jdbcType}" />
 			% endif 
		% endfor
  	</resultMap>
  	<resultMap id="${class_name}DTOResultMap" type="com.${package_name}.${module_name}.api.dto.${class_name}DTO" extends="${class_name}ResultMap">
  	</resultMap>

	<sql id="columns">
		${',\n\t\t'.join(colums) }
  	</sql>

	<sql id="columns_as">
		${',\n\t\t'.join(colums_as) }
  	</sql>

    <select id="pageList" resultType="com.${package_name}.${module_name}.api.dto.${class_name}DTO">
    	SELECT <include refid="columns_as" /> FROM ${table_name}
    </select>

    <select id="selectById" resultType="com.${package_name}.${module_name}.api.dto.${class_name}DTO" parameterType="java.lang.String">
        SELECT
        <include refid="columns_as" />
        FROM ${table_name}
        WHERE id = #{id}
    </select>

    <insert id="insert" parameterType="com.${package_name}.${module_name}.service.entity.${class_name}DO">
        INSERT INTO ${table_name} (<include refid="columns" />)
        VALUES
        (${',\n\t\t'.join(values)})
    </insert>

    <update id="update" parameterType="com.${package_name}.${module_name}.service.entity.${class_name}DO">
        UPDATE ${table_name}
        <set>
        	% for index in  range(len(fields)):
            <if test="${fields[index].name} != null">
                ${fields[index].field }= #{${fields[index].name}, jdbcType=${fields[index].jdbcType}},
            </if>
			% endfor
        </set>
        WHERE id = #{id}
    </update>
</mapper>