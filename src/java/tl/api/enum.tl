package ${java_class.package};

import com.guns21.common.enums.ValuableEnum;
import lombok.Getter;

@Getter
public enum ${java_class.class_name} implements ValuableEnum {
	% if len(java_class.fields)==0 :
	;
	% endif 
	% for index in  range(len(java_class.fields)):
	% if index < len(java_class.fields)-1 :
 		<% spl=',' %>
 	% else:
 		<% spl=';' %>
 	% endif 
 	ENUM_${java_class.fields[index].name.capitalize()}(Byte.parseByte("${java_class.fields[index].name}"),"${java_class.fields[index].comment}")${spl}
	% endfor

	private Byte value;
    private String desc;

    ${java_class.class_name}(Byte value, String desc) {
        this.value = value;
        this.desc = desc;
    }


}