package ${java_class.package};
<%
	hasId = java_class.has_id
	id_Field =java_class.id_field
	class_name = java_class.class_name
%>
% if hasId:
	% if id_Field.type == "String" :
import com.guns21.support.entity.StringIDEntity;
	% elif id_Field.type == "Long":
import com.guns21.support.entity.LongIDEntity;
	% else :
import com.guns21.support.entity.StringIDEntity;
	% endif
% endif 
import lombok.AllArgsConstructor;
import lombok.experimental.SuperBuilder;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

import java.io.Serializable;
${java_class.imports}

% for a in java_class.fields:
	% if a.name in []:
		<% enumType = table.entity_name+a.name[0].upper() + a.name[1:] + "Enum" %>
import ${java_class.module_package}.api.enums.${enumType};
	% endif
% endfor
import ${java_class.module_package}.api.dto.${java_class.original_class_name}DTO;

/**
 * ${java_class.comment}
 */
@SuperBuilder(toBuilder = true)
@AllArgsConstructor
@NoArgsConstructor
% if hasId:
@ToString(callSuper = true)
% else:
@ToString
% endif
% if hasId:
@EqualsAndHashCode(callSuper = true)
% else:
@EqualsAndHashCode
% endif
@Setter
@Getter
% if hasId:
	% if id_Field.type == "String" :
public class ${class_name} extends StringIDEntity {
	% elif id_Field.type == "Long":
public class ${class_name} extends LongIDEntity {
	% else :
public class ${class_name} extends StringIDEntity {
	% endif
% else:
public class ${class_name} implements Serializable {
% endif 

% for a in java_class.fields:
	<% 
	enumType = a.type
	if a.name in []:
		enumType = table.entity_name+a.name[0].upper() + a.name[1:] + "Enum"
	%>
	% if hasId:
		% if a.name not in ["id","gmt_created","gmt_modified"]:

	/**
		* ${a.comment}
		* ${a.note}
		*/
	private ${enumType} ${a.name};
		% endif
	% else :

	/**
		* ${a.comment}
		* ${a.note}
		*/
	private ${enumType} ${a.name};
	%endif
% endfor

	public static ${class_name} from(${java_class.original_class_name}DTO dto) {
		return  ${class_name}Transformer.INSTANCE.from(dto);
	}

    @Mapper
    public interface  ${class_name}Transformer {
        ${class_name}Transformer INSTANCE = Mappers.getMapper( ${class_name}Transformer.class);

		${class_name} from(${java_class.original_class_name}DTO dto);

    }
}