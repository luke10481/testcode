package com.example.demo;

import freemarker.core.TemplateClassResolver;
import org.springframework.context.annotation.Configuration;
import org.springframework.beans.factory.annotation.Autowired;

import javax.annotation.PostConstruct;

@Configuration
public class FreemarkerConfig {

    @Autowired
    private freemarker.template.Configuration configuration;

    @PostConstruct
    public void postConstruct() {
        configuration.setAPIBuiltinEnabled(true);
        configuration.setNewBuiltinClassResolver(TemplateClassResolver.UNRESTRICTED_RESOLVER);
        // add other configuration settings if needed
    }
}

