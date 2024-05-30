package ${java_class.package};
<%
    has_id = java_class.has_id
    class_name =java_class.original_class_name
    id_field = java_class.id_field
%>
import java.util.Optional;
import java.util.Objects;
import java.util.List;
import com.guns21.common.util.ObjectUtils;

import org.springframework.stereotype.Repository;
import org.springframework.beans.factory.annotation.Autowired;

import ${java_class.module_package}.service.repository.${class_name}Repository;
import ${java_class.module_package}.service.repository.mapper.${class_name}Mapper;
import ${java_class.module_package}.service.entity.${class_name}DO;

@Repository
public class ${class_name}RepositoryImpl implements ${class_name}Repository {
	
	@Autowired
	private ${class_name}Mapper mapper;

	@Override
    public Integer insert(${class_name}DO data) {
        return Optional.ofNullable(data).map(entity -> {
            % if has_id:
            entity.preCreate();
            % endif
            return mapper.insert(entity);
        }).orElse(0);
    }

    @Override
    public Integer insertSelective(${class_name}DO data) {
        return Optional.ofNullable(data).map(entity -> {
            % if has_id:
            entity.preCreate();
            % endif
            return mapper.insertSelective(entity);
        }).orElse(0);
    }

    @Override
    public Integer insertBatch(List<${class_name}DO> data) {
        return mapper.insertBatch(data);
    }

	@Override
    public Integer updateByPrimaryKey(${class_name}DO data) {
        return Optional.ofNullable(data).map(entity -> {
            % if has_id:
            entity.preUpdate();
            % endif
            return mapper.updateByPrimaryKey(entity);
        }).orElse(0);
    }

    @Override
    public Integer updateByPrimaryKeySelective(${class_name}DO data) {
        return Optional.ofNullable(data).map(entity -> {
            % if has_id:
            entity.preUpdate();
            % endif
            return mapper.updateByPrimaryKeySelective(entity);
        }).orElse(0);
    }

% if has_id:
	@Override
    public Integer deleteByPrimaryKey(${id_field.type} ${id_field.name}) {
        % if id_field.type == "String" :
        if (ObjectUtils.hasText(id)) {
        % elif id_field.type == "Long":
        if (Objects.nonNull(id)) {
        % endif
            return mapper.deleteByPrimaryKey(id);
        }
    	return 0;
    }
% endif
}