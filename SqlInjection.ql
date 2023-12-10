import python
import semmle.python.security.dataflow.SqlInjectionQuery
import SqlInjectionFlow::PathGraph
private import semmle.python.ApiGraphs

private module SqlInjectionConfig implements DataFlow::ConfigSig {


  predicate isSource(DataFlow::Node source) {
    source instanceof Source
  }

  private API::Node dbClient() {
    result = API::moduleImport("dbutils").getMember("pooled_db").getMember("PooledDB").getReturn()
  }

  private API::Node connection() {
    result = dbClient().getMember("connection")
  }

  private API::CallNode parser() {
    result = API::moduleImport("defusedxml").getMember("ElementTree").getMember("parse").getACall()
  }

  predicate isSink(DataFlow::Node sink) { 
    sink instanceof Sink or 
    (sink = parser().getParameter(0, "source").asSink() and parser().getParameter(2, "forbid_dtd").getAValueReachingSink().asExpr().(ImmutableLiteral).booleanValue() = false)
  }

  predicate isBarrier(DataFlow::Node node) { node instanceof Sanitizer }
}

/** Global taint-tracking for detecting "SQL injection" vulnerabilities. */
module SqlInjectionFlow = TaintTracking::Global<SqlInjectionConfig>;

from SqlInjectionFlow::PathNode source, SqlInjectionFlow::PathNode sink
where SqlInjectionFlow::flowPath(source, sink)
select sink.getNode(), source, sink, "This SQL query depends on a $@.", source.getNode(),
  "user-provided value"
