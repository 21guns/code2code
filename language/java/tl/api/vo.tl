package com.${package_name}.${action.module_name}.api.vo;

import lombok.AllArgsConstructor;
import lombok.experimental.SuperBuilder;
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

/**
 * ${action.comment}
 */
@SuperBuilder(toBuilder = true)
@AllArgsConstructor
@NoArgsConstructor
@ToString
@EqualsAndHashCode
@Setter
@Getter

public class ${action.class_name}VO implements Serializable {

	% for a in action.response:
	/**
 	 * ${a.comment}
	 */
	private ${a.type} ${a.name};

	% endfor


}