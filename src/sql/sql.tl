% for table in tables:
<%
    statms = []
    columns = ',\n\t'.join(map(lambda x : "`" + x.name + "` " + x.type + " NOT NULL COMMENT "+ "'" + x.comment+"'", table.fields))
    statms.append(columns)
    for p in table.pk:
        statms.append("PRIMARY KEY (`" + p.name + "`)")
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
