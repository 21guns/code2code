package ${java_class.package};

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import lombok.extern.slf4j.Slf4j;

import com.guns21.data.domain.result.MessageResult;
import com.guns21.data.domain.result.PageData;

import ${java_class.module_package}.api.dto.*;
/**
 * 
 */
@RestController
@Slf4j
${java_class.annotations}
public class ${java_class.class_name} {
	% for a in java_class.methods:
	
	/**
 	 * ${a.comment}
	 */
	${a.annotations}
    public MessageResult ${a.method_name}(${a.params}) {

		return MessageResult.success();
	}
	% endfor

}