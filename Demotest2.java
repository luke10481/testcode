package com.example;

import org.dom4j.Document;
import org.dom4j.Element;
import java.io.File;
import org.dom4j.io.SAXReader;

public class Demotest2 {

    public static void main(String[] args) {
        try {
            String xmlFile = "C:\\Users\\luke10481\\IdeaProjects\\sql注入靶场\\src\\main\\resources\\static\\Data.xml";
            SAXReader reader = new SAXReader();
            Document document = reader.read(new File(xmlFile));
            Element root = document.getRootElement();
            Element id = root.element("content");
            System.out.println("id: " + id.getTextTrim());
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}