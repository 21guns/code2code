package com.${package_name}.${module_name}.service.service.impl;
<%!
    import utils
%>
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import lombok.extern.slf4j.Slf4j;
import com.${package_name}.${module_name}.service.service.${utils.firstUpower(module_name)}QueryService;
import com.guns21.data.domain.result.PageData;
% for a in actions:
    % if a.is_get_method():
        % if a.has_request():
import com.${package_name}.${module_name}.api.dto.${a.class_name}DTO;
        % endif
        % if a.has_response():
import com.${package_name}.${module_name}.api.vo.${a.class_name}VO;
        % endif
    % endif
% endfor
/**
 * @author jliu
 * @date
 */
@Service
@Slf4j
public class ${utils.firstUpower(module_name)}QueryServiceImpl implements ${utils.firstUpower(module_name)}QueryService {

    //@Autowired Mapper
    % for a in actions:
        % if a.is_get_method() :
        
    /**
     * ${a.comment}
     */
    public  ${a.get_service_method_return_type()} ${a.get_method_name()}(${a.get_service_method_params()}) {
        //TODO
        return null;
    } 
        % endif 
    % endfor


}