package com.example;

import org.apache.commons.digester3.Digester;
import org.apache.commons.digester3.Rule;
import org.xml.sax.Attributes;
import org.xml.sax.SAXException;

import java.io.File;
import java.io.IOException;

public class Demotest3 {

    public static void main(String[] args) {
        try {
            String xmlFile = "C:\\Users\\luke10481\\IdeaProjects\\sql注入靶场\\src\\main\\resources\\static\\Data2.xml";
            Digester digester = new Digester();
            digester.setValidating(false);

            StringBuilder idBuilder = new StringBuilder();
            digester.addRule("school/student/id", new Rule() {
                @Override
                public void body(String namespace, String name, String text) throws SAXException {
                    idBuilder.append(text);
                }
            });

            digester.parse(new File(xmlFile));

            System.out.println("id: " + idBuilder.toString());
        } catch (IOException | SAXException e) {
            System.out.println(e);
        }
    }
}