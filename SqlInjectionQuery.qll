/**
 * Provides a taint-tracking configuration for detecting "SQL injection" vulnerabilities.
 *
 * Note, for performance reasons: only import this file if
 * `SqlInjection::Configuration` is needed, otherwise
 * `SqlInjectionCustomizations` should be imported instead.
 */

private import python
private import semmle.python.ApiGraphs
import semmle.python.dataflow.new.DataFlow
import semmle.python.dataflow.new.TaintTracking
import SqlInjectionCustomizations::SqlInjection
import semmle.python.dataflow.new.internal.TypeTrackingImpl

/**
 * DEPRECATED: Use `SqlInjectionFlow` module instead.
 *
 * A taint-tracking configuration for detecting "SQL injection" vulnerabilities.
 */
deprecated class Configuration extends TaintTracking::Configuration {
  Configuration() { this = "SqlInjection" }

  override predicate isSource(DataFlow::Node source) { source instanceof Source }

  override predicate isSink(DataFlow::Node sink) { sink instanceof Sink }

  override predicate isSanitizer(DataFlow::Node node) { node instanceof Sanitizer }
}

private module SqlInjectionConfig implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) { 
    source instanceof Source
  }

  predicate isSink(DataFlow::Node sink) { sink instanceof Sink or 
    sink = API::moduleImport("pandas").getMember("read_sql").getACall().getParameter(0).asSink() }

  predicate isBarrier(DataFlow::Node node) { node instanceof Sanitizer }

  predicate isAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
    exists(int n, int i, FunctionObject funcobj, DataFlow::Node argsNode, Tuple tuple, Class cls|
      not funcobj.getAMethodCall().getScope().getLocation().getFile().inStdlib()
      and exists(funcobj.getAMethodCall().getKwargs())
      and argsNode.asCfgNode() = funcobj.getAMethodCall().getStarArg()
      and argsNode.getALocalSource().asExpr() = tuple
      and cls.containsInScope(funcobj.getFunction())
      and n = count(funcobj.getFunction().getArgs().getAnItem())
      and i in [0 .. n]
      and (
        (nodeTo.asExpr() = funcobj.getFunction().getArgs().getItem(i+1)
        and nodeFrom.asExpr() = tuple.getElt(i))
        or
        (nodeTo.asExpr() = funcobj.getFunction().getArgs().getItem(0)
        and nodeFrom.asExpr() = funcobj.getAMethodCall().getNode().getFunc().(Attribute).getObject*())
        or
        (nodeTo.asExpr() = cls.getInitMethod().getArgs().getItem(0)
        and nodeFrom.asExpr() = funcobj.getAMethodCall().getNode().getFunc().(Attribute).getObject*())
        or
        (nodeTo.asCfgNode() = funcobj.getFunction().getAFlowNode()
        and nodeFrom.asCfgNode() = funcobj.getAMethodCall())
      )
    )
  }
}

class FilterJumpStep extends TypeTrackingInput::AdditionalCapturedJumpStep {
  /**
   * Holds if data can flow from `pred` to `succ` via a callback chain.
   */

  predicate test(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
    exists(Attribute attr, SelfAttributeStore store, Assign assign|
      attr.getObject().toString() = assign.getATarget().toString()
      and attr.getName() = store.getName()
      and assign.getValue() = store.getClass().getClassObject().getACall().getNode()
      and nodeFrom.asExpr() = attr
      and nodeTo.asExpr() = store.getAssignedValue()
    )
  }

  predicate test2(Assign assign, string str) {
    exists( |
      //and objNode.getALocalSource().asExpr() = store.getClass().getClassObject().getACall().getNode()
      assign.getATarget().toString() = str
      )
  }
  
  override predicate othercapturedjumpstep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
        // Class Base:
    //  var = expr
    //  ...
    //  def f(self):
    //    ...self.var is used...
    //
    // Class Sub(Base):
    //  def g(self):
    //    ...self.var is used...
    //
    // nodeFrom is `expr`
    // nodeTo is entry node for `self.var`
    exists(SelfAttributeRead read, Class baseClass, Class subClass |
      baseClass.contains(nodeFrom.asExpr()) and
      (
        exists(ClassObject subClassObj |
          subClassObj.getABaseType*() = baseClass.getClassObject() and 
          subClassObj = subClass.getClassObject()
        )
        or
        subClass = baseClass
      )
      and
      subClass.contains(read) and 
      read.getName() = nodeFrom.asExpr().toString() and
      nodeTo.asCfgNode() = read.getAFlowNode() 
    )
    // Class Base:
    //   def __init__(self, expr=expr):
    //     self.var = expr
    //
    //   def f(self):
    //     ...self.var is used...
    // 
    // Class Sub(Base):
    //   def g(self):
    //     ...self.var is used...
    //
    // nodeFrom is `expr`
    // nodeTo is entry node for `self.var`
    or
    exists(SelfAttributeStore store, SelfAttributeRead read, Class subClass |
      nodeFrom.asExpr() = store.getAssignedValue() and 
      (
        exists(Class baseClass, ClassObject subClassObj |
          baseClass = store.getClass() and 
          subClassObj.getABaseType*() = baseClass.getClassObject() and 
          subClassObj = subClass.getClassObject()
        )
        or
        subClass = store.getClass()
      )
      and
      subClass.contains(read) and
      read.getName() = store.getName() and
      nodeTo.asCfgNode() = read.getAFlowNode()
    )
    or
    exists(Attribute attr, SelfAttributeStore store, Assign assign|
      attr.getObject().toString() = assign.getATarget().toString()
      and attr.getName() = store.getName()
      and assign.getValue() = store.getClass().getClassObject().getACall().getNode()
      and nodeFrom.asExpr() = store.getAssignedValue()
      and nodeTo.asExpr() = attr
    )
    or
    exists(int n, int i, FunctionObject funcobj, DataFlow::Node argsNode, Tuple tuple, Class cls|
      not funcobj.getAMethodCall().getScope().getLocation().getFile().inStdlib()
      and exists(funcobj.getAMethodCall().getKwargs())
      and argsNode.asCfgNode() = funcobj.getAMethodCall().getStarArg()
      and argsNode.getALocalSource().asExpr() = tuple
      and cls.containsInScope(funcobj.getFunction())
      and n = count(funcobj.getFunction().getArgs().getAnItem())
      and i in [0 .. n]
      and (
        (nodeTo.asExpr() = funcobj.getFunction().getArgs().getItem(i+1)
        and nodeFrom.asExpr() = tuple.getElt(i))
        or
        (nodeTo.asExpr() = funcobj.getFunction().getArgs().getItem(0)
        and nodeFrom.asExpr() = funcobj.getAMethodCall().getNode().getFunc().(Attribute).getObject*())
        or
        (nodeTo.asExpr() = cls.getInitMethod().getArgs().getItem(0)
        and nodeFrom.asExpr() = funcobj.getAMethodCall().getNode().getFunc().(Attribute).getObject*())
        or
        (nodeTo.asCfgNode() = funcobj.getFunction().getAFlowNode()
        and nodeFrom.asCfgNode() = funcobj.getAMethodCall())
      )
    )
  }
}

/** Global taint-tracking for detecting "SQL injection" vulnerabilities. */
module SqlInjectionFlow = TaintTracking::Global<SqlInjectionConfig>;
