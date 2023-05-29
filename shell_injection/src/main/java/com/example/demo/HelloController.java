package com.example.demo;

import freemarker.cache.MultiTemplateLoader;
import freemarker.cache.StringTemplateLoader;
import freemarker.cache.TemplateLoader;
import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateException;
import freemarker.template.utility.DateUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.StringWriter;
import java.util.HashMap;
import java.util.Map;

@Controller
public class HelloController {

    @Autowired
    private  Configuration con;

    @GetMapping("/")
    public String index() {
        return "index";
    }

    @RequestMapping(value = "/hello")
    public String hello(@RequestBody Map<String,Object> body, Model model) {
        model.addAttribute("name", body.get("name"));
        return "hello";
    }

    @RequestMapping(value = "/freemarker")
    public void freemarker(@RequestParam("username") String username, HttpServletRequest httpserver,HttpServletResponse response) {
        try{
            String data = "1ooooooooooooooooooo~";
            String templateContent = "<html><body>Hello " + username + " ${data}</body></html>";
            String html = createHtmlFromString(templateContent,data);
            response.getWriter().println(html);

        }catch (Exception e){
            e.printStackTrace();
        }
    }

    private String createHtmlFromString(String templateContent, String data) throws IOException, TemplateException {
        Configuration cfg = new Configuration();
        StringTemplateLoader stringLoader = new StringTemplateLoader();
        stringLoader.putTemplate("myTemplate",templateContent);
        cfg.setTemplateLoader(stringLoader);
        Template template = cfg.getTemplate("myTemplate","utf-8");
        Map root = new HashMap();
        root.put("data",data);

        StringWriter writer = new StringWriter();
        template.process(root,writer);
        return writer.toString();
    }

    @RequestMapping(value = "/template", method =  RequestMethod.POST)
    public String template(@RequestBody Map<String,String> templates) throws IOException {
        StringTemplateLoader stringLoader = new StringTemplateLoader();
        for(String templateKey : templates.keySet()){
            stringLoader.putTemplate(templateKey, templates.get(templateKey));
        }
        con.setTemplateLoader(new MultiTemplateLoader(new TemplateLoader[]{stringLoader,
                con.getTemplateLoader()}));
        return "index";
    }
}