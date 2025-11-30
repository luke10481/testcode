import java
import semmle.code.java.dataflow.FlowSources
import semmle.code.java.dataflow.TaintTracking
import semmle.code.java.security.ExternalAPIs
import UntrustedDataToExternalApiFlow::PathGraph

string test() {
  exists(ClassOrInterface interfaceClass,Method interfaceMethod, 
    Annotation parentpath, Annotation subpath,
    Annotation jalorResource, Annotation jalorOperation,
    Class implClass,Method implMethod|
    implClass.contains(implMethod)
    and implClass.extendsOrImplements(interfaceClass)
    and jalorResource = implClass.getAnAnnotation()
    and jalorResource.getType().hasQualifiedName("com.example.demo.annotation", "JalorResource")
    and jalorOperation = implMethod.getAnAnnotation()
    and jalorOperation.getType().hasQualifiedName("com.example.demo.annotation", "JalorOperation")
    and interfaceMethod.getName() = implMethod.getName()
    and interfaceClass.contains(interfaceMethod)
    and interfaceClass.getAnAnnotation() = parentpath
    and parentpath.getType().hasQualifiedName("javax.ws.rs", "Path")
    and interfaceMethod.getAnAnnotation() = subpath
    and subpath.getType().hasQualifiedName("javax.ws.rs", "Path")
    |
    result = parentpath.getValue("value").toString().replaceAll("\"", "") +
    subpath.getValue("value").toString().replaceAll("\"", "") +
    implClass.getName() + implMethod.getName()
    )
}

// predicate test3() {
//     exists(Method interfaceMethod, Method implMethod, RefType interfaceType|
//     interfaceMethod.getDeclaringType() = interfaceType and
//     interfaceType.isInternal()
//     |result= )
// }

predicate test2(string astr) {
  astr = ["classa$methoda","classb$methodb"]
  and "classb"= astr.substring(0, astr.indexOf("$"))
  and  "methoda" = astr.substring(astr.indexOf("$") + 1, astr.length())
}

import java

from Method interfaceMethod, Method implMethod
where
  // 接口方法在接口中
  interfaceMethod.getDeclaringType().isInternal() and
  // 实现类方法覆盖了接口方法
  implMethod.overrides*(interfaceMethod) and
  // 方法名相同（可选约束）
  interfaceMethod.getName() = implMethod.getName()
select 
  interfaceMethod.getDeclaringType().getName() + "." + interfaceMethod.getName() +
  " <- 被实现为 -> " + 
  implMethod.getDeclaringType().getName() + "." + implMethod.getName()