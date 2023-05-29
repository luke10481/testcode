package com.example.demo;

import freemarker.core.TemplateClassResolver;
import freemarker.template.Configuration;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {

	public static void main(String[] args) {
		//Configuration cfg = new Configuration();
		//cfg.setAPIBuiltinEnabled(true);	// 開啟api
		//cfg.setNewBuiltinClassResolver(TemplateClassResolver.UNRESTRICTED_RESOLVER);
		SpringApplication.run(DemoApplication.class, args);
	}
}