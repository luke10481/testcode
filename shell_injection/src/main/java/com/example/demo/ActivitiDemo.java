package com.example.demo;

import org.activiti.engine.ProcessEngine;
import org.activiti.engine.RepositoryService;
import org.activiti.engine.RuntimeService;
import org.activiti.engine.impl.cfg.StandaloneInMemProcessEngineConfiguration;

public class ActivitiDemo {

    public static void main (String[] args) {

        // Build engine and deploy
        ProcessEngine processEngine = new StandaloneInMemProcessEngineConfiguration().buildProcessEngine();
        RepositoryService repositoryService = processEngine.getRepositoryService();
        repositoryService.createDeployment().addClasspathResource("process.bpmn20.xml").deploy();

        // Start process instance
        RuntimeService runtimeService = processEngine.getRuntimeService();
        runtimeService.startProcessInstanceByKey("myProcess");
    }
}