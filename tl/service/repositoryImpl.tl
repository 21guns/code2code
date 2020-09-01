package com.${package_name}.${module_name}.service.repository.impl;
<%!
    import utils
%>
import org.springframework.stereotype.Repository;
import org.springframework.beans.factory.annotation.Autowired;
import com.${package_name}.${module_name}.service.repository.${utils.firstUpower(module_name)}Repository;
% for a in actions:
    % if a.has_request() and not a.is_get_method():
import com.${package_name}.${module_name}.api.dto.${a.class_name}DTO;
    % endif
% endfor

@Repository
public class ${utils.firstUpower(module_name)}RepositoryImpl implements ${utils.firstUpower(module_name)}Repository {

	//@Autowired Mapper
    % for a in actions:
        % if not a.is_get_method() :
        
    /**
     * ${a.comment}
     */
    public Integer  ${a.get_method_name()}(${a.get_service_method_params()}) {
        //TODO
        return 0;
    } 
        % endif 
    % endfor


}