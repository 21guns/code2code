package com.${package_name}.${module_name}.api.vo;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.io.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Objects;
% for a in table.fields:
	% if a.name in ['type','status']:
		<% enumType = table.entity_name+a.name[0].upper() + a.name[1:] + "Enum" %>
import com.${package_name}.${module_name}.api.enums.${enumType};
	% endif
% endfor
/**
 * ${table.comment}
 */
@Builder(toBuilder = true)
@AllArgsConstructor
@NoArgsConstructor
@EqualsAndHashCode
@ToString
@Setter
@Getter
public class ${class_name} implements Serializable {
 

	% for a in table.fields:
		<% 
		enumType = a.type
		if a.name in ['type','status']:
			enumType = table.entity_name+a.name[0].upper() + a.name[1:] + "Enum"
		%>
	/**
 	 * ${a.comment}
 	 * ${a.note}
	 */
	private ${enumType} ${a.name};
	% endfor


}