package com.example;

import org.dom4j.Document;
import org.dom4j.Element;
import java.io.File;
import org.dom4j.io.SAXReader;

public class Demotest2 {

    public static void main(String[] args) {
        try {
            String xmlFile = "C:\\Users\\luke10481\\IdeaProjects\\sql注入靶场\\src\\main\\resources\\static\\Data2.xml";
            SAXReader reader = new SAXReader();
            Document document = reader.read(new File(xmlFile));
            Element root = document.getRootElement();
            Element student = root.element("student");
            Element id = student.element("id");
            System.out.println("id: " + id.getTextTrim());
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}