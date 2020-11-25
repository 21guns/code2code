package ${java_class.package};

import lombok.AllArgsConstructor;
import lombok.experimental.SuperBuilder;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.io.Serializable;
${java_class.imports}

/**
 * ${java_class.comment}
 */
@SuperBuilder(toBuilder = true)
@AllArgsConstructor
@NoArgsConstructor
@ToString
@EqualsAndHashCode
@Setter
@Getter

public class ${java_class.class_name} implements Serializable {

	% for a in java_class.fields:
	/**
 	 * ${a.comment}
	 */
	private ${a.type} ${a.name};

	% endfor


}