package com.example;

import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import javax.xml.stream.XMLStreamReader;
import java.io.FileInputStream;


public class Demotest {

    public static void main(String[] args) {
        try {
            String xmlFile = "C:\\Users\\luke10481\\IdeaProjects\\sql注入靶场\\src\\main\\resources\\static\\Data.xml";
            // Intentionally make the XMLInputFactory vulnerable to XXE
            XMLInputFactory factory = XMLInputFactory.newFactory();
            factory.setProperty(XMLInputFactory.SUPPORT_DTD, true);
            factory.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, true);

            XMLStreamReader reader = factory.createXMLStreamReader(new FileInputStream(xmlFile));

            while (reader.hasNext()) {
                int eventType = reader.next();

                if (eventType == XMLStreamConstants.START_ELEMENT && "content".equals(reader.getLocalName())) {
                    String content = reader.getElementText();
                    System.out.println("Extracted content: \n" + content);
                }
            }

            reader.close();
        }catch (Exception e){
            System.out.println(e);
        }
    }
}