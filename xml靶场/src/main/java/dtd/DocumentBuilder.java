package dtd;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.IOException;

public class DocumentBuilder {
    public static void main(String[] args) {
        try {
            String xmlFile = "Data.xml";
            // Intentionally make the DocumentBuilderFactory vulnerable to XXE
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", false);
            factory.setFeature("http://xml.org/sax/features/external-general-entities", true);
            factory.setFeature("http://xml.org/sax/features/external-parameter-entities", true);
            factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", true);

            javax.xml.parsers.DocumentBuilder builder = factory.newDocumentBuilder();
            Document document = builder.parse(new File(xmlFile));

            NodeList contentNodeList = document.getElementsByTagName("content");

            if (contentNodeList.getLength() > 0) {
                Element contentElement = (Element) contentNodeList.item(0);
                String content = contentElement.getTextContent();
                System.out.println("Extracted content: \n" + content);
            }

        } catch (ParserConfigurationException | IOException | org.xml.sax.SAXException e) {
            System.out.println(e);
        }
    }
}
