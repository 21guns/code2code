<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >
<mapper namespace="${java_class.package}.${java_class.class_name}" >
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
		table_name = java_class.metadata_name
		fields = java_class.fields
		class_name =java_class.original_class_name

		for index in  range(len(fields)):

			colums_as_line = ', '.join(map(lambda x : (x.field + " AS " + x.name) if x.field != x.name else x.field, fields[colums_as_start:index]))
			if len(colums_as_line) > COLUMNS_LINE_MAX :
				colums_as.append(colums_as_line)
				colums_as_start = index

			colums_line = ', '.join(map(lambda x : x.field, fields[colums_start:index]))
			if len(colums_line) > COLUMNS_LINE_MAX :
				colums.append(colums_line)
				colums_start = index

			values_line = ', '.join(map(lambda x : "#{" + x.name +", jdbcType=" + x.jdbc_type + "}", fields[values_start:index]))
			if len(values_line) > COLUMNS_LINE_MAX :
				values.append(values_line)
				values_start = index

		colums_as_line = ', '.join(map(lambda x : (x.field + " AS " + x.name) if x.field != x.name else x.field, fields[colums_as_start:]))
		if (len(colums_as_line)) > 0:
			colums_as.append(colums_as_line)

		colums_line = ', '.join(map(lambda x : x.field, fields[colums_start:]))
		if (len(colums_line)) > 0:
			colums.append(colums_line)

		values_line = ', '.join(map(lambda x : "#{" + x.name +", jdbcType=" + x.jdbc_type + "}", fields[values_start:]))
		if (len(values_line)) > 0:
			values.append(values_line)
	%>
	<resultMap id="${class_name}ResultMap" type="${java_class.module_package}.api.vo.${class_name}VO" >
		% for index in  range(len(fields)):
			% if fields[index].name == "id" :
		<id column="id" property="id" jdbcType="${fields[index].jdbc_type}" />
			% else:
		<result column="${fields[index].field}" property="${fields[index].name}" jdbcType="${fields[index].jdbc_type}" />
 			% endif 
		% endfor
  	</resultMap>

	<sql id="columns">
		${',\n\t\t'.join(colums) }
  	</sql>

	<sql id="columns_as">
		${',\n\t\t'.join(colums_as) }
  	</sql>

    <select id="pageList" resultMap="${class_name}ResultMap">
    	SELECT <include refid="columns_as" /> FROM ${table_name}
    </select>

% if java_class.has_id :
    <select id="selectByPrimaryKey" parameterType="${java_class.id_field.type}" resultMap="${class_name}ResultMap">
        SELECT
        <include refid="columns" />
        FROM ${table_name}
        WHERE id = #{id,jdbcType=${java_class.id_field.jdbc_type}}
    </select>

    <delete id="deleteByPrimaryKey" parameterType="java.lang.Long">
        DELETE FROM ${table_name} WHERE id = #{id,jdbcType=${java_class.id_field.jdbc_type}}
    </delete>
% endif

    <insert id="insert" parameterType="${java_class.project_package}.entity.${class_name}DO">
        INSERT INTO ${table_name} (<include refid="columns" />)
        VALUES
        (${',\n\t\t'.join(values)})
    </insert>

    <insert id="insertSelective" parameterType="${java_class.project_package}.entity.${class_name}DO">
        INSERT INTO ${table_name}
	 	<trim prefix="(" suffix=")" suffixOverrides=",">
	      % for index in  range(len(fields)):
         	<if test="${fields[index].name} != null">
                ${fields[index].field },
            </if>
			% endfor
	    </trim>
	    <trim prefix="values (" suffix=")" suffixOverrides=",">
        	% for index in  range(len(fields)):
            <if test="${fields[index].name} != null">
                #{${fields[index].name}, jdbcType=${fields[index].jdbc_type}},
            </if>
			% endfor
    	</trim>
	</insert>

	<update id="updateByPrimaryKey" parameterType="${java_class.project_package}.entity.${class_name}DO">
	    UPDATE ${table_name}
	    <set>
	       % for index in  range(len(fields)):
	        ${fields[index].field }= #{${fields[index].name}, jdbcType=${fields[index].jdbc_type}},
			% endfor
	    </set>
	    WHERE id = #{id,jdbcType=BIGINT}
 	</update>

    <update id="updateByPrimaryKeySelective" parameterType="${java_class.project_package}.entity.${class_name}DO">
        UPDATE ${table_name}
        <set>
        	% for index in  range(len(fields)):
            <if test="${fields[index].name} != null">
                ${fields[index].field }= #{${fields[index].name}, jdbcType=${fields[index].jdbc_type}},
            </if>
			% endfor
        </set>
        WHERE id = #{id}
    </update>
</mapper>