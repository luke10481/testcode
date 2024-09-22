import python
import semmle.python.security.dataflow.SqlInjectionQuery
import semmle.python.frameworks.Flask
import SqlInjectionFlow::PathGraph
private import semmle.python.dataflow.new.internal.DataFlowPublic as DataFlowPublic
class Node = DataFlowPublic::Node;

Node getRouteNode() {
    result = [
        Flask::FlaskApp::instance().getMember("route").getACall(),
        Flask::Blueprint::instance().getMember("route").getACall()
    ]
}

Node getClassNode() {
    result = [
        Flask::FlaskApp::classRef().getACall(),
    ]
}

predicate test(Function routeFunc) {
    exists(Node noAuthClassNode|
        routeFunc.getADecorator() = getNoAuthClassNode().asExpr() 
        and not exists(Function authFunc |
            authFunc.getADecorator().(Attribute).getName() = "login_required"
            |routeFunc = authFunc
        )
    )
}

Node getNoAuthClassNode() {
    exists(Node noAuthClassNode, API::Node flaskNode|
        noAuthClassNode = getClassNode()
        and not exists( Function globalFunc, Node globalNode|
            globalFunc.getADecorator().(Attribute).getName() = "before_request"
            and globalFunc.getName().toLowerCase().matches("%soa%")
            and globalFunc.getADecorator().(Attribute).getObject() = globalNode.asExpr()
            and noAuthClassNode.getALocalSource().flowsTo(globalNode)
        )
        | 
        flaskNode = [
            Flask::FlaskApp::instance(),
            Flask::Blueprint::instance()
        ]
        and flaskNode.asSource() = noAuthClassNode
        and result = [
            flaskNode.getMember("route").getACall()
        ]
    )
}

predicate test3(Function routeFunc ) {
    not exists(Function authFunc | 
        routeFunc = authFunc
    )
}
from Function routeFunc
where exists(| 
    routeFunc.getADecorator() = getRouteNode().asExpr() 

)
select routeFunc