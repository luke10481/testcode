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

predicate flaskAppAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
    exists(DataFlow::MethodCallNode mcn|
        nodeFrom = mcn.getAMethodCall("register_blueprint").getArg(0)
        and nodeTo = mcn.getAMethodCall("register_blueprint").getObject()
    )
}

module FlaskGlobalConfiguration implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node source) {
        source = Flask::FlaskApp::instance().asSource()
    }
  
    predicate isSink(DataFlow::Node sink) {
        sink = getGlobalNode("before_request")
    }

    predicate isAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
        flaskAppAdditionalFlowStep(nodeFrom, nodeTo)
    }
}
module FlaskGlobalFlow = DataFlow::Global<FlaskGlobalConfiguration>;

module BlueprintGlobalRegisterConfiguration implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node source) {
        source = getGlobalNode("before_app_request")
    }
  
    predicate isSink(DataFlow::Node sink) {
        sink = Flask::FlaskApp::instance().getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink()
    }

    predicate isAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
        flaskAppAdditionalFlowStep(nodeFrom, nodeTo)
    }
}
module BlueprintGlobalRegisterFlow = DataFlow::Global<BlueprintGlobalRegisterConfiguration>;

module BlueprintPartAuthConfiguration implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node source) {
        source = Flask::Blueprint::instance().asSource()
    }
  
    predicate isSink(DataFlow::Node sink) {
        sink = getGlobalNode("before_request")
    }

    predicate isAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
        flaskAppAdditionalFlowStep(nodeFrom, nodeTo)
    }
}
module BlueprintPartAuthFlow = DataFlow::Global<BlueprintPartAuthConfiguration>;

module BlueprintGlobalAuthConfiguration implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node source) {
        source = Flask::Blueprint::instance().asSource()
    }
  
    predicate isSink(DataFlow::Node sink) {
        sink = getGlobalNode("before_app_request")
    }

    predicate isAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
        flaskAppAdditionalFlowStep(nodeFrom, nodeTo)
    }
}
module BlueprintGlobalAuthFlow = DataFlow::Global<BlueprintGlobalAuthConfiguration>;

module BlueprintRegisterFlaskAppConfiguration implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node source) {
        source = Flask::Blueprint::instance().asSource()
    }
  
    predicate isSink(DataFlow::Node sink) {
        sink = Flask::FlaskApp::instance().getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink()
    }

    predicate isAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
        flaskAppAdditionalFlowStep(nodeFrom, nodeTo)
    }
}
module BlueprintRegisterFlaskAppFlow = DataFlow::Global<BlueprintRegisterFlaskAppConfiguration>;

module BlueprintRegisterBlueprintConfiguration implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node source) {
        source = Flask::Blueprint::instance().asSource()
    }
  
    predicate isSink(DataFlow::Node sink) {
        sink = Flask::Blueprint::instance().getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink()
    }

    predicate isAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
        flaskAppAdditionalFlowStep(nodeFrom, nodeTo)
    }
}
module BlueprintRegisterBlueprintFlow = DataFlow::Global<BlueprintRegisterBlueprintConfiguration>;

DataFlow::Node getBluePrintPartAuth(){
    exists(API::Node noAuthBluePrintNode|
        noAuthBluePrintNode = Flask::Blueprint::instance()
        and BlueprintPartAuthFlow::flow(noAuthBluePrintNode.asSource(), getGlobalNode("before_request"))
        |result = noAuthBluePrintNode.getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink()
    )
}

DataFlow::Node getBluePrintGlobalAuth(){
    exists(API::Node noAuthBluePrintNode, API::Node noAuthFlaskAppNode|
        noAuthBluePrintNode = Flask::Blueprint::instance()
        and noAuthFlaskAppNode = Flask::FlaskApp::instance()
        and BlueprintGlobalAuthFlow::flow(noAuthBluePrintNode.asSource(), getGlobalNode("before_app_request"))
        |result = noAuthFlaskAppNode.getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink()
    )
}

module BlueprintPartAuthRegisterBlueprintConfiguration implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node source) {
        source = Flask::Blueprint::instance().asSource()
    }
  
    predicate isSink(DataFlow::Node sink) {
        sink = getBluePrintPartAuth()
    }

    predicate isAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
        flaskAppAdditionalFlowStep(nodeFrom, nodeTo)
    }
}
module BlueprintPartAuthRegisterBlueprintFlow = DataFlow::Global<BlueprintPartAuthRegisterBlueprintConfiguration>;

module BlueprintGlobalAuthRegisterBlueprintConfiguration implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node source) {
        source = Flask::Blueprint::instance().asSource()
    }
  
    predicate isSink(DataFlow::Node sink) {
        sink = getBluePrintGlobalAuth()
    }

    predicate isAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
        flaskAppAdditionalFlowStep(nodeFrom, nodeTo)
    }
}
module BlueprintGlobalAuthRegisterBlueprintFlow = DataFlow::Global<BlueprintGlobalAuthRegisterBlueprintConfiguration>;

DataFlow::Node getNoAuthClassNode() {
    exists(API::Node noAuthFlaskNode, API::Node noAuthBluePrintNode|
        noAuthFlaskNode = Flask::FlaskApp::instance()
        and noAuthBluePrintNode = Flask::Blueprint::instance()
        and not exists(|FlaskGlobalFlow::flow(noAuthFlaskNode.asSource(), getGlobalNode("before_request")))
        and not exists(|BlueprintGlobalRegisterFlow::flow(getGlobalNode("before_app_request"), noAuthFlaskNode.getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink()))
        and not exists(|BlueprintPartAuthFlow::flow(noAuthBluePrintNode.asSource(), getGlobalNode("before_request")))
        and not exists(|BlueprintPartAuthRegisterBlueprintFlow::flow(noAuthBluePrintNode.asSource(), getBluePrintPartAuth()))
        and if exists(|BlueprintRegisterFlaskAppFlow::flow(noAuthBluePrintNode.asSource(), noAuthFlaskNode.getMember("register_blueprint").getACall().getParameter(0, "blueprint").asSink())
        )
        then result = noAuthBluePrintNode.getMember("route").getACall()
        else result = noAuthFlaskNode.getMember("route").getACall()
    )
}

DataFlow::Node testxx() {
    exists(API::Node noAuthFlaskNode, API::Node noAuthBluePrintNode|
        noAuthFlaskNode = Flask::FlaskApp::instance()
        and noAuthBluePrintNode = Flask::Blueprint::instance()
       
        and if exists(|
            BlueprintGlobalAuthRegisterBlueprintFlow::flow(noAuthBluePrintNode.asSource(), getBluePrintGlobalAuth())
        )
        then result = noAuthBluePrintNode.getMember("route").getACall()
        else result = noAuthFlaskNode.getMember("route").getACall()
    )
}

from Function routeFunc
where exists(| 
    routeFunc.getADecorator() = getNoAuthClassNode().asExpr() 
)
select routeFunc