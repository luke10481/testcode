package com.example;

import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

import javax.xml.XMLConstants;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;
import java.io.File;

public class Demotest8 {
    public static void main(String[] args) {
        try {
            String schemaFile = "C:\\Users\\luke10481\\IdeaProjects\\sql注入靶场\\src\\main\\resources\\static\\schema.xsd";
            String xmlFile = "C:\\Users\\luke10481\\IdeaProjects\\sql注入靶场\\src\\main\\resources\\static\\Data.xml";

            // Intentionally make the SAXParserFactory vulnerable to XXE
            SAXParserFactory factory = SAXParserFactory.newInstance();
            factory.setFeature("http://xml.org/sax/features/external-general-entities", true);
            factory.setFeature("http://xml.org/sax/features/external-parameter-entities", true);
            factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", false);
            factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", true);

            // Set the schema for validation
            SchemaFactory schemaFactory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
            Schema schema = schemaFactory.newSchema(new File(schemaFile));
            factory.setSchema(schema);

            SAXParser parser = factory.newSAXParser();
            parser.parse(new File(xmlFile), new DefaultHandler() {
                private boolean inContent = false;

                @Override
                public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {
                    if ("content".equals(qName)) {
                        inContent = true;
                    }
                }

                @Override
                public void endElement(String uri, String localName, String qName) throws SAXException {
                    if ("content".equals(qName)) {
                        inContent = false;
                    }
                }

                @Override
                public void characters(char[] ch, int start, int length) throws SAXException {
                    if (inContent) {
                        String content = new String(ch, start, length);
                        System.out.println("Extracted content: \n" + content);
                    }
                }
            });

        } catch (Exception e) {
            System.out.println(e);
        }
    }
}