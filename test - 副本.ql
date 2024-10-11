import python
import semmle.python.ApiGraphs
import semmle.python.frameworks.Flask

module EnvironmentToFileConfiguration implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node source) {
        //source = Flask::Blueprint::classRef().getReturn().asSource()
        exists(Function globalFunc, DataFlow::Node globalNode|
            globalFunc.getADecorator().(Attribute).getName() = "before_app_request"
            and globalFunc.getName().toLowerCase().matches("%soa%")
            and globalFunc.getADecorator().(Attribute).getObject() = globalNode.asExpr()
            |source = globalNode
        )
    }
  
    predicate isSink(DataFlow::Node sink) {
        sink = Flask::FlaskApp::classRef().getReturn().getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink()
        // exists(Function globalFunc, DataFlow::Node globalNode|
        //     globalFunc.getADecorator().(Attribute).getName() = "before_app_request"
        //     and globalFunc.getName().toLowerCase().matches("%soa%")
        //     and globalFunc.getADecorator().(Attribute).getObject() = globalNode.asExpr()
        //     |sink = globalNode
        // )
    }
}
  
module EnvironmentToFileFlow = DataFlow::Global<EnvironmentToFileConfiguration>;

module EnvironmentToFileConfiguration2 implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node source) {
        source = Flask::Blueprint::classRef().getReturn().asSource()
    }
  
    predicate isSink(DataFlow::Node sink) {
        sink = Flask::FlaskApp::classRef().getReturn().getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink()
    }
}
  
module EnvironmentToFileFlow2 = DataFlow::Global<EnvironmentToFileConfiguration2>;

DataFlow::Node getRouteNode() {
    result = [
        Flask::FlaskApp::instance().getMember("route").getACall(),
        Flask::Blueprint::instance().getMember("route").getACall()
    ]
}

// predicate test(Function routeFunc) {
//     exists(DataFlow::Node noAuthClassNode|
//         routeFunc.getADecorator() = getNoAuthClassNode().asExpr() 
//         and not exists(Function authFunc |
//             authFunc.getADecorator().(Attribute).getName() = "login_required"
//             |routeFunc = authFunc
//         )
//     )
// }

API::Node getNoAuthClassNode() {
    exists(API::Node noAuthFlaskNode, API::Node noAuthBluePrintNode|
        noAuthFlaskNode = Flask::FlaskApp::classRef()
        and noAuthBluePrintNode = Flask::Blueprint::classRef()
        and not exists(Function globalFunc, DataFlow::Node globalNode|
            globalFunc.getADecorator().(Attribute).getName() = "before_request"
            and globalFunc.getName().toLowerCase().matches("%soa%")
            and globalFunc.getADecorator().(Attribute).getObject() = globalNode.asExpr()
            and noAuthFlaskNode.getACall().getALocalSource().flowsTo(globalNode)
        )
        and not exists(Function globalFunc, DataFlow::Node globalNode|
            globalFunc.getADecorator().(Attribute).getName() = "before_app_request"
            and globalFunc.getName().toLowerCase().matches("%soa%")
            and globalFunc.getADecorator().(Attribute).getObject() = globalNode.asExpr()
            and EnvironmentToFileFlow::flow(globalNode, noAuthFlaskNode.getReturn().getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink())
        )
        // and exists(Function globalFunc, DataFlow::Node globalNode|
        //     globalFunc.getADecorator().(Attribute).getName() = "before_request"
        //     and globalFunc.getName().toLowerCase().matches("%soa%")
        //     and globalFunc.getADecorator().(Attribute).getObject() = globalNode.asExpr()
        //     and EnvironmentToFileFlow::flow(globalNode, noAuthFlaskNode.getReturn().getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink())
        // )
        and EnvironmentToFileFlow2::flow(noAuthBluePrintNode.getReturn().asSource(), noAuthFlaskNode.getReturn().getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink())
        |result = [noAuthFlaskNode,noAuthBluePrintNode]
    )
}

API::Node getNoAuthClassNode(API::Node noAuthFlaskNode) {
    exists(API::Node noAuthBluePrintNode, Function globalFunc, DataFlow::Node globalNode|
        noAuthFlaskNode = Flask::FlaskApp::classRef()
        and noAuthBluePrintNode = Flask::Blueprint::classRef()

            and globalFunc.getADecorator().(Attribute).getName() = "before_request"
            and globalFunc.getName().toLowerCase().matches("%soa%")
            and globalFunc.getADecorator().(Attribute).getObject() = globalNode.asExpr()
            and noAuthFlaskNode.getACall().getALocalSource().flowsTo(globalNode)
        |result = noAuthFlaskNode
    )
}

API::Node getNoAuthClassNode2(API::Node noAuthFlaskNode) {
    exists(API::Node noAuthBluePrintNode, Function globalFunc, DataFlow::Node globalNode|
        noAuthFlaskNode = Flask::FlaskApp::classRef()
        and noAuthBluePrintNode = Flask::Blueprint::classRef()
        and globalFunc.getADecorator().(Attribute).getName() = "before_app_request"
        and globalFunc.getName().toLowerCase().matches("%soa%")
        and globalFunc.getADecorator().(Attribute).getObject() = globalNode.asExpr()
        and EnvironmentToFileFlow::flow(globalNode, noAuthFlaskNode.getReturn().getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink())
        //and noAuthFlaskNode.getACall().getALocalSource().flowsTo(globalNode)
        |result = noAuthFlaskNode
    )
}

predicate test3(DataFlow::Node routeFunc) {
    routeFunc = Flask::FlaskApp::instance().asSource()
}



predicate test4(DataFlow::Node av, DataFlow::Node bv) {
    // av.asCfgNode().getNode().toString().matches("abc")
    // and bv.asCfgNode().getNode().toString().matches("p")
   EnvironmentToFileFlow::flow(av, bv)
}

predicate test5(DataFlow::Node av, DataFlow::Node bv) {
    av.asCfgNode().getNode().toString().matches("p")
    and bv.asCfgNode().getNode().toString().matches("abc")
    and DataFlow::localFlowStep*(av, bv)
}

from Function routeFunc
where exists(| 
    routeFunc.getADecorator() = getRouteNode().asExpr() 

)
select routeFunc