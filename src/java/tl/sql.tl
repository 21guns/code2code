% for table in tables:
<%
    statms = []
    columns = ',\n\t'.join(map(lambda x : "`" + x.name + "` " + x.databaseType + " NOT NULL COMMENT "+ "'" + x.comment+"'", table.fields))
    statms.append(columns)
    if table.has_id():
        statms.append("PRIMARY KEY (`" + table.get_id_field().name + "`)")
%>
-- -----------------------------------------------
-- Table `${table.name}` ${table.comment}
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS `${table.name}` (
    ${',\n\t'.join(statms)}
)
ENGINE = InnoDB DEFAULT CHARACTER SET utf8
COMMENT = '${table.comment}';
% endfor
