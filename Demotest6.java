package com.example;

import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;

import java.io.File;
import java.io.IOException;

public class Demotest6 {
    public static void main(String[] args) {
        try {
            String xmlFile = "C:\\Users\\luke10481\\IdeaProjects\\sql注入靶场\\src\\main\\resources\\static\\Data.xml";
            SAXBuilder saxBuilder = new SAXBuilder();
            saxBuilder.setFeature("http://xml.org/sax/features/external-general-entities", true);
            saxBuilder.setFeature("http://xml.org/sax/features/external-parameter-entities", true);
            Document document = saxBuilder.build(new File(xmlFile));

            Element root = document.getRootElement();
            Element id = root.getChild("content");
            System.out.println("id: " + id.getTextTrim());
        } catch (JDOMException | IOException e) {
            System.out.println(e);
        }
    }
}