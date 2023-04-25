package com.example;

import org.apache.commons.io.FileUtils;
import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;
import org.xml.sax.SAXException;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

public class Demotest4 {
    public static void main(String[] args) {
        try {
            String xmlFile = "C:\\Users\\luke10481\\IdeaProjects\\sql注入靶场\\src\\main\\resources\\static\\Data3.xml";
            String xmlContent = FileUtils.readFileToString(new File(xmlFile), StandardCharsets.UTF_8);

            // Parse the XML content
            Document document = DocumentHelper.parseText(xmlContent);
            Element root = document.getRootElement();
            Element student = root.element("student");
            Element id = student.element("id");
            System.out.println("id: " + id.getTextTrim());
        } catch (IOException | DocumentException e) {
            System.out.println(e);
        }
    }
}