package com.example;

import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import java.io.File;
import java.io.IOException;

public class Demotest5 {
    public static void main(String[] args) {
        try {
            String xmlFile = "C:\\Users\\luke10481\\IdeaProjects\\sql注入靶场\\src\\main\\resources\\static\\Data.xml";
            SAXParserFactory factory = SAXParserFactory.newInstance();
            factory.setFeature("http://xml.org/sax/features/external-general-entities", true);
            factory.setFeature("http://xml.org/sax/features/external-parameter-entities", true);
            SAXParser saxParser = factory.newSAXParser();

            DefaultHandler handler = new DefaultHandler() {
                private boolean idElement = false;

                @Override
                public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {
                    if ("content".equalsIgnoreCase(qName)) {
                        idElement = true;
                    }
                }

                @Override
                public void characters(char[] ch, int start, int length) throws SAXException {
                    if (idElement) {
                        System.out.println("id: " + new String(ch, start, length));
                        idElement = false;
                    }
                }
            };

            saxParser.parse(new File(xmlFile), handler);
        } catch (ParserConfigurationException | SAXException | IOException e) {
            System.out.println(e);
        }
    }
}