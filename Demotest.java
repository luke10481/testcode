package com.example;

import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import javax.xml.stream.XMLStreamReader;
import java.io.FileInputStream;


public class Demotest {

    public static void main(String[] args) {
        try {
            String xmlFile = "C:\\Users\\luke10481\\IdeaProjects\\sql注入靶场\\src\\main\\resources\\static\\Data.xml";
            XMLInputFactory xmlInputFactory = XMLInputFactory.newFactory();

            // Enable DTD support and external entity resolution
            xmlInputFactory.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, true);
            xmlInputFactory.setProperty(XMLInputFactory.SUPPORT_DTD, true);

            XMLStreamReader xmlReader = xmlInputFactory.createXMLStreamReader(new FileInputStream(xmlFile));
            while (xmlReader.hasNext()) {
                int eventType = xmlReader.next();

                if (eventType == XMLStreamConstants.START_ELEMENT) {
                    if ("Girl".equals(xmlReader.getLocalName())) {
                        String name = xmlReader.getAttributeValue(null, "name");
                        String age = xmlReader.getAttributeValue(null, "age");
                        System.out.println("a neme called " + name + "girl， age is" + age);
                    }
                } else if (eventType == XMLStreamConstants.CHARACTERS) {
                    // Print the text content of the "Girl" element
                    String text = xmlReader.getText().trim();
                    if (!text.isEmpty()) {
                        System.out.println("Text content: " + text);
                    }
                }
            }
        }catch (Exception e){
            System.out.println(e);
        }
    }
}