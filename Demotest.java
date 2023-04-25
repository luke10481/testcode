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
            xmlInputFactory.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, true);
            xmlInputFactory.setProperty(XMLInputFactory.SUPPORT_DTD, true);

            XMLStreamReader xmlReader = xmlInputFactory.createXMLStreamReader(new FileInputStream(xmlFile));
            while (xmlReader.hasNext()) {
                int eventType = xmlReader.next();

                if (eventType == XMLStreamConstants.START_ELEMENT) {
                    if ("id".equals(xmlReader.getLocalName())) {
                        xmlReader.next(); // Move to the text content of the "id" element
                        String idContent = xmlReader.getText();
                        System.out.println("id: " + idContent);
                    }
                }
            }
        }catch (Exception e){
            System.out.println(e);
        }
    }
}