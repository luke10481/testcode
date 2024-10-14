import python
import semmle.python.ApiGraphs
import semmle.python.frameworks.Flask


DataFlow::Node getGlobalNode(string decorator){
    exists(Function globalFunc, DataFlow::Node globalNode|
        globalFunc.getADecorator().(Attribute).getName() = decorator
        and globalFunc.getName().toLowerCase().matches("%soa%")
        and globalFunc.getADecorator().(Attribute).getObject() = globalNode.asExpr()
        |result = globalNode
    )
}

module BlueprintGlobalRegisterConfiguration implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node source) {
        source = getGlobalNode("before_app_request")
    }
  
    predicate isSink(DataFlow::Node sink) {
        sink = Flask::FlaskApp::classRef().getReturn().getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink()
    }
}
module BlueprintGlobalRegisterFlow = DataFlow::Global<BlueprintGlobalRegisterConfiguration>;

module BlueprintRegisterConfiguration implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node source) {
        source = Flask::Blueprint::classRef().getReturn().asSource()
    }
  
    predicate isSink(DataFlow::Node sink) {
        sink = Flask::FlaskApp::classRef().getReturn().getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink()
    }
}
module BlueprintRegisterFlow = DataFlow::Global<BlueprintRegisterConfiguration>;

module BlueprintPartConfiguration implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node source) {
        source = Flask::Blueprint::classRef().getReturn().asSource()
    }
  
    predicate isSink(DataFlow::Node sink) {
        sink = getGlobalNode("before_request")
    }
}
module BlueprintPartFlow = DataFlow::Global<BlueprintPartConfiguration>;

module FlaskGlobalConfiguration implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node source) {
        source = Flask::FlaskApp::classRef().getReturn().asSource()
    }
  
    predicate isSink(DataFlow::Node sink) {
        sink = getGlobalNode("before_request")
    }
}
module FlaskGlobalFlow = DataFlow::Global<FlaskGlobalConfiguration>;

DataFlow::Node getNoAuthClassNode() {
    exists(API::Node noAuthFlaskNode, API::Node noAuthBluePrintNode|
        noAuthFlaskNode = Flask::FlaskApp::classRef().getReturn()
        and noAuthBluePrintNode = Flask::Blueprint::classRef().getReturn()
        and not exists(|FlaskGlobalFlow::flow(noAuthFlaskNode.asSource(), getGlobalNode("before_request")))
        and not exists(|BlueprintGlobalRegisterFlow::flow(getGlobalNode("before_app_request"), noAuthFlaskNode.getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink()))
        and not exists(|BlueprintPartFlow::flow(noAuthBluePrintNode.asSource(), getGlobalNode("before_request")))
        and if exists(|BlueprintRegisterFlow::flow(noAuthBluePrintNode.asSource(), noAuthFlaskNode.getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink()))
        then result = noAuthBluePrintNode.getMember("route").getACall()
        else result = noAuthFlaskNode.getMember("route").getACall()
    )
}

from Function routeFunc
where exists(| 
    routeFunc.getADecorator() = getNoAuthClassNode().asExpr() 
)
select routeFunc